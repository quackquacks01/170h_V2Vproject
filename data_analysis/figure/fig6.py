import pandas as pd
import folium

# CSV 파일 불러오기 
df = pd.read_csv("rcpi_speed") 

# 위경도 정규화
df['Latitude'] = df['Rla'] / 1e7
df['Longitude'] = df['Rlo'] / 1e7

# 조건 필터링: 속도 ≤ 10, RCPI ≤ 100
df_filtered = df[(df['Speed(km/h)'] <= 10) & (df['RCPI'] <= 100)]

# 지도 중심 위치 설정 (중간값 기준)
center_lat = df_filtered['Latitude'].mean()
center_lon = df_filtered['Longitude'].mean()

# folium 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=17)

# 마커 추가
for _, row in df_filtered.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=4,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup=f"Speed: {row['Speed(km/h)']:.1f} km/h<br>RCPI: {row['RCPI']}"
    ).add_to(m)

# HTML로 저장
m.save("low_speed_low_rcpi_map.html")
