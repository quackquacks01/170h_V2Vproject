import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 경로
df = pd.read_csv('output1_4.csv')

# 위도/경도 값 소수점으로 변환 (10^7로 나누기)
df['Tla'] = df['Tla'] / 10**7  # 송신기 위도
df['Tlo'] = df['Tlo'] / 10**7  # 송신기 경도

# 곡선 구간 범위 설정
latitude_min = 37.408544  # 위도 최소값
latitude_max = 37.408927  # 위도 최대값
longitude_min = 127.095553  # 경도 최소값
longitude_max = 127.096021  # 경도 최대값

# 데이터 필터링 (곡선 구간 범위 내에 있는 데이터만 추출)
filtered_df = df[(df['Tla'] >= latitude_min) & (df['Tla'] <= latitude_max) &
                 (df['Tlo'] >= longitude_min) & (df['Tlo'] <= longitude_max)]

# 그림 17 곡선 거리 히스토그램
plt.figure(figsize=(10, 6))
filtered_df['Distance'].plot(kind='hist', bins=20, color='skyblue', edgecolor='black')
plt.title('Distance Histogram - Central Vertical Path')
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 그림 18 곡선 구간 거리 vs RCPI 산점도
plt.figure(figsize=(10, 6))
sns.scatterplot(x=filtered_df['Distance'], y=filtered_df['RCPI'], color='blue')
plt.title('Scatter Plot: Distance vs RCPI')
plt.xlabel('Distance')
plt.ylabel('RCPI')
plt.tight_layout()
plt.show()
