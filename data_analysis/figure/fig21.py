import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 파일 로드
df = pd.read_csv('output1_4.csv')  

# 2. 위경도 변환 (필요한 경우에만)
df['Latitude'] = df['Rla'] / 10**7
df['Longitude'] = df['Rlo'] / 10**7

# 3. Time을 datetime 형식으로 변환
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')

# 4. Time을 인덱스로 설정
df.set_index('Time', inplace=True)

# 5. 30분 단위로 리샘플링하여 RCPI 평균 계산
rcpi_by_time_30min = df.resample('30T')['RCPI'].mean()

# 6. 결과 출력 (각 30분 구간별 RCPI 평균)
print(rcpi_by_time_30min)

# 7. 그래프 시각화
plt.figure(figsize=(10, 6))
rcpi_by_time_30min.plot(kind='bar', color='skyblue')
plt.title("Average RCPI by 30-Minute Intervals")
plt.xlabel("Time (HH:MM)")
plt.ylabel("Average RCPI")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
