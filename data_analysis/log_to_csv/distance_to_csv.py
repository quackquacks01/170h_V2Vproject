import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 읽기
df = pd.read_csv("output0.csv")
print(df.head())  # 데이터 확인

# 위도/경도 변환: 10⁷로 나눠 소수점 형태로 변환
df['Tx_Latitude'] = df['Tx_Latitude'] / 10**7
df['Tx_Longitude'] = df['Tx_Longitude'] / 10**7
df['Rx_Latitude'] = df['Rx_Latitude'] / 10**7
df['Rx_Longitude'] = df['Rx_Longitude'] / 10**7

# 거리 계산 함수 (haversine 공식을 사용)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371e3  # 지구 반지름 (미터)
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c  # 거리 (미터)

# 송수신기 간 거리 계산
df['Distance'] = haversine(df['Tx_Latitude'], df['Tx_Longitude'], df['Rx_Latitude'], df['Rx_Longitude'])

# 거리 값만 추출하여 새로운 DataFrame 생성 (이 부분 추가)
distance_df = df[['Distance']]  # 'Distance' 열만 추출
distance_df.to_csv("distance_only.csv", index=False)  # 새로운 CSV 파일로 저장
print("Distances saved to 'distance_only.csv'")
