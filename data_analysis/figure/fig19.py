import pandas as pd
import folium
from folium.plugins import MarkerCluster

df = pd.read_csv(r"C:\Users\wah43\vehicle_map_project\output1_4_removed_fixed_spot.csv")

# RCPI ≥ 160 필터링
high_rcpi_df = df[df["RCPI"] >= 170]

# 지도 초기 위치 (판교 주변 평균 좌표)
center_lat = high_rcpi_df["Rla"].mean()
center_lon = high_rcpi_df["Rlo"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

# 클러스터로 그룹핑해서 시각화
marker_cluster = MarkerCluster().add_to(m)

# Marker 추가
for _, row in high_rcpi_df.iterrows():
    popup_text = (
        f"RCPI: {row['RCPI']}<br>"
        f"Distance: {row['Distance']} m<br>"
        f"Latency: {row['Latency (ms)']} ms<br>"
        f"RSSI: {row['RSSI']}"
    )
    folium.Marker(
        location=[row["Rla"], row["Rlo"]],
        popup=popup_text,
        icon=folium.Icon(color="green", icon="signal", prefix="fa")
    ).add_to(marker_cluster)

m.save("high_rcpi_locations_map.html")