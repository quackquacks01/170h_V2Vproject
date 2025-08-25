
'''
본 프로그램은 송신 차량과 수신 차량의 위치를 지도 위에 실시간으로 시각화하고, 
통신 품질 지표(RCPI, 지연 시간 등)를 함께 표시하는 애니메이션 대시보드입니다. 
특정 세션(SN코드)을 선택하고, 시간 슬라이더 또는 자동 재생 기능을 통해 통신 품질 흐름을 확인할 수 있습니다.
'''

import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import base64
import math

# 아이콘 이미지를 base64로 인코딩
def encode_icon_to_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return "data:image/png;base64," + base64.b64encode(data).decode()

# 송신/수신 차량 아이콘 설정
sender_icon_url = encode_icon_to_base64("sender_car.png")
receiver_icon_url = encode_icon_to_base64("receiver_car.png")

# 지도 API 키 설정
pdk.settings.mapbox_api_key = "pk.eyJ1IjoicXVhY2txdWFjayIsImEiOiJjbWE0dWRuczIwOWtzMmtwc3R6YnlrMjY3In0.ADVgeMdjFlhXeDEX8YQyBA"  # ← 여기에 키 넣기

# 데이터 불러오기 (캐시 사용)
@st.cache_data
def load_data():
    df = pd.read_csv("output1_4_removed_fixed_spot.csv")
    df = df[['File', 'Tla', 'Tlo', 'Rla', 'Rlo', 'RCPI', 'Distance', 'Latency (ms)', 'Time']].dropna()
    df["Session"] = df["File"].str.extract(r"(SN\d+)")
    return df

df = load_data()

# 세션 선택
unique_sessions = sorted(df["Session"].dropna().unique())
selected_session = st.selectbox("📁 데이터 구간 선택 (SN코드 기준)", unique_sessions)
df = df[df["Session"] == selected_session]

# 초기 상태 설정
if "frame" not in st.session_state:
    st.session_state.frame = 0
if "playing" not in st.session_state:
    st.session_state.playing = False

# 현재 시간 프레임 추출
times = df["Time"].unique().tolist()
if not times:
    st.warning("선택한 날짜에 데이터가 없습니다.")
    st.stop()

current_time = times[st.session_state.frame]
st.title("🚗 차량 간 통신 애니메이션")
st.write(f"🕒 현재 시간: {current_time}")
frame_data = df[df["Time"] == current_time]

# 두 좌표 간 방향 계산
def calculate_bearing(lat1, lon1, lat2, lon2):
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    x = math.sin(dLon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    bearing = math.atan2(x, y)
    return (math.degrees(bearing) + 360) % 360

# 지도 위에 차량 위치 및 선, 텍스트 표시
if not frame_data.empty:
    row = frame_data.iloc[0]
    tx_lat, tx_lon = row["Tla"] / 1e7, row["Tlo"] / 1e7
    rx_lat, rx_lon = row["Rla"], row["Rlo"]
    angle_tx = (calculate_bearing(tx_lat, tx_lon, rx_lat, rx_lon) - 90) % 360
    angle_rx = angle_tx

    # 정보 텍스트 생성
    info_label = f"RCPI: {row['RCPI']} / {row['Distance']}m / Latency: {row['Latency (ms)']}ms"
    text_df = pd.DataFrame([{
        "coordinates": [(tx_lon + rx_lon) / 2, (tx_lat + rx_lat) / 2],
        "label": info_label
    }])

    # 송수신 차량 위치 데이터 생성
    sender_df = pd.DataFrame([{
        "lon": tx_lon,
        "lat": tx_lat,
        "angle": angle_tx,
        "icon_url": sender_icon_url
    }])
    receiver_df = pd.DataFrame([{
        "lon": rx_lon,
        "lat": rx_lat,
        "angle": angle_rx,
        "icon_url": receiver_icon_url
    }])
    for df_icon in [sender_df, receiver_df]:
        df_icon["icon_data"] = df_icon.apply(lambda row: {
            "url": row["icon_url"],
            "width": 64,
            "height": 64,
            "anchorY": 32,  # 중앙
            "anchorX": 32,
        }, axis=1)

    # 선 (통신 경로) 데이터 생성
    line_df = pd.DataFrame([{
        "start_lon": tx_lon,
        "start_lat": tx_lat,
        "end_lon": rx_lon,
        "end_lat": rx_lat,
        "rcpi": row["RCPI"],
        "distance": row["Distance"],
        "time": row["Time"]
    }])

    # pydeck 레이어 생성
    line_layer = pdk.Layer(
        "LineLayer",
        data=line_df,
        get_source_position=["start_lon", "start_lat"],
        get_target_position=["end_lon", "end_lat"],
        get_color="[255 - rcpi, rcpi, 100]",
        get_width=5,
        pickable=True,
    )

    icon_layer_tx = pdk.Layer(
        "IconLayer",
        data=sender_df,
        get_icon="icon_data",
        get_position=["lon", "lat"],
        get_size=4,
        size_scale=15,
        get_angle="angle",
        pickable=False,
    )

    icon_layer_rx = pdk.Layer(
        "IconLayer",
        data=receiver_df,
        get_icon="icon_data",
        get_position=["lon", "lat"],
        get_size=4,
        size_scale=15,
        get_angle="angle",
        pickable=False,
    )

    text_layer = pdk.Layer(
        "TextLayer",
        data=text_df,
        get_position="coordinates",
        get_text="label",
        get_color=[255, 255, 255],
        get_size=16,
        get_alignment_baseline="'bottom'",
    )

    # 지도에 차트 출력
    st.pydeck_chart(pdk.Deck(
        layers=[line_layer, icon_layer_tx, icon_layer_rx, text_layer],
        initial_view_state=pdk.ViewState(
            latitude=tx_lat,
            longitude=tx_lon,
            zoom=16,
            pitch=45,
        ),
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={"html": "<b>시간:</b> {time}<br><b>RCPI:</b> {rcpi}<br><b>거리:</b> {distance}m"},
    ))

# 슬라이더로 시간 이동
frame_index = st.slider("🧭 시간 이동", 0, len(times) - 1, st.session_state.frame)
st.session_state.frame = frame_index

# 재생 / 정지 버튼
col1, col2 = st.columns(2)
if col1.button("▶️ 재생"):
    st.session_state.playing = True
if col2.button("⏸️ 정지"):
    st.session_state.playing = False

# 재생 중이면 프레임 자동 증가
if st.session_state.playing:
    time.sleep(0.6)
    st.session_state.frame = (st.session_state.frame + 1) % len(times)
    st.rerun()
