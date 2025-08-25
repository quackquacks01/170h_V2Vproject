import pandas as pd
import numpy as np
from datetime import datetime

# CSV 파일 불러오기
df = pd.read_csv("output1_4_removed_fixed_spot.csv")  # 네 원본 파일 이름

# 1. 중복된 Time 제거 (처음 것만 남기고 원래 순서 유지)
df_unique = df.drop_duplicates(subset='Time', keep='first').copy().reset_index(drop=True)

# 2. Time을 datetime으로 변환 (정렬은 하지 않음)
df_unique['ParsedTime'] = pd.to_datetime(df_unique['Time'], format='%H:%M:%S')

# 3. 거리 계산 (Haversine 공식)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

lat = df_unique['Rla'].values
lon = df_unique['Rlo'].values
distances = [0]

for i in range(1, len(df_unique)):
    d = haversine(lat[i-1], lon[i-1], lat[i], lon[i])
    distances.append(d)

df_unique['DistanceDelta(m)'] = distances

# 4. 시간 차이 계산 (순서 유지 + 자정 넘긴 경우 보정)
parsed_times = df_unique['ParsedTime'].tolist()
timedeltas = [0]
for i in range(1, len(parsed_times)):
    delta = (parsed_times[i] - parsed_times[i-1]).total_seconds()
    if delta < 0:
        delta += 86400  # 하루 넘어간 것 처리
    timedeltas.append(delta)
df_unique['TimeDelta(s)'] = timedeltas

# 5. 속도 계산 (m/s → km/h)
df_unique['Speed(km/h)'] = (df_unique['DistanceDelta(m)'] / df_unique['TimeDelta(s)'].replace(0, np.nan)) * 3.6
df_unique['Speed(km/h)'] = df_unique['Speed(km/h)'].fillna(0)

# 6. 필요한 열만 저장
export_cols = ['Time', 'Rla', 'Rlo', 'RCPI', 'DistanceDelta(m)', 'TimeDelta(s)', 'Speed(km/h)']
df_unique[export_cols].to_csv("rcpi_with_speed_calculated_ordered.csv", index=False)
