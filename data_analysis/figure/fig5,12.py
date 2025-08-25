import pandas as pd
import folium
from folium.plugins import HeatMap

# CSV 파일 불러오기
df = pd.read_csv("output1_4.csv")

# 좌표 정규화 (1e7로 나누기)
df['Rla'] = df['Rla'] * 1e-7
df['Rlo'] = df['Rlo'] * 1e-7

# 중심 위치 설정
map_center = [df['Rla'].mean(), df['Rlo'].mean()]
m = folium.Map(location=map_center, zoom_start=15, tiles='cartodbpositron')  # 더 깔끔한 배경

# HeatMap 생성용 데이터: [lat, lon, weight]
heat_data = [
    [row['Rla'], row['Rlo'], row['RSSI']]
    for _, row in df.iterrows()
    if not pd.isna(row['RSSI'])  # 결측치 제거
]

# RSSI 정규화 (선택): 너무 큰 값이면 가중치 0~1로 스케일링
# df['RSSI_norm'] = (df['RSSI'] - df['RSSI'].min()) / (df['RSSI'].max() - df['RSSI'].min())
# heat_data = [[row['Rla'], row['Rlo'], row['RSSI_norm']] for _, row in df.iterrows()]

# HeatMap 추가
HeatMap(
    heat_data,
    radius=8,      # 퍼짐 정도: 작을수록 선명
    blur=4,         # 흐림 정도: 작을수록 또렷
    max_zoom=17,    # 줌될 때까지 유지
    min_opacity=0.4 # 최소 투명도
).add_to(m)

# 저장
m.save("signal_heatmap.html")
