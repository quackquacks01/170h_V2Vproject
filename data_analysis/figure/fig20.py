# 이제 RCPI 비교쌍 분석을 위해 csv 내에 있는 'Distance' 열을 사용하여 그룹화
# Distance를 기준으로 소수점 첫째자리로 그룹핑한 뒤, 각 그룹에서 RCPI 가장 높은 지점과 가장 낮은 지점을 연결

import pandas as pd
import folium

# CSV 불러오기
df = pd.read_csv(r"C:\Users\wah43\vehicle_map_project\output1_4_removed_fixed_spot.csv")
df = df[['Rla', 'Rlo', 'RCPI', 'Distance', 'Time']].dropna()

# 거리 값을 소수점 첫째 자리로 반올림하여 그룹핑 키 생성
df["DistanceGroup"] = df["Distance"].round(1)

# 그룹별 RCPI 최대/최소 점 추출
connection_rows = []
for group, group_df in df.groupby("DistanceGroup"):
    if len(group_df) < 2:
        continue
    high = group_df.loc[group_df["RCPI"].idxmax()]
    low = group_df.loc[group_df["RCPI"].idxmin()]
    if high["RCPI"] == low["RCPI"]:
        continue  # 동일 RCPI는 제외
    connection_rows.append((high, low, group))  # 거리 그룹도 같이 저장

# 지도 생성
m = folium.Map(location=[df["Rla"].mean(), df["Rlo"].mean()], zoom_start=15)

# 점 및 선 추가
for high, low, dist in connection_rows:
    # 초록 점: 높은 RCPI
    folium.Marker(
        location=[high["Rla"], high["Rlo"]],
        popup=f"HIGH RCPI: {high['RCPI']}",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)

    # 빨간 점: 낮은 RCPI
    folium.Marker(
        location=[low["Rla"], low["Rlo"]],
        popup=f"LOW RCPI: {low['RCPI']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # 선 연결
    folium.PolyLine(
        locations=[[high["Rla"], high["Rlo"]], [low["Rla"], low["Rlo"]]],
        color='orange',
        weight=2
    ).add_to(m)

m.save("equal_distance_rcpi_dif_map.html")
