import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
df = pd.read_csv('output1_4.csv')

# 'Rla'와 'Rlo'를 실제 위도, 경도로 변환
df['Latitude'] = df['Rla'] / 10**7
df['Longitude'] = df['Rlo'] / 10**7

# 위경도 범위 설정
lat_min = 37.402887
lat_max = 37.403706
lon_min = 127.104979
lon_max = 127.105708

# 위경도 범위 내의 데이터만 필터링
filtered_df = df[
    (df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) &
    (df['Longitude'] >= lon_min) & (df['Longitude'] <= lon_max)
]

# 필터링된 데이터가 있는지 확인
if filtered_df.empty:
    print("No data available in the specified latitude and longitude range.")
else:
    # 'Time'을 시간 형식으로 변환
    filtered_df['Time'] = pd.to_datetime(filtered_df['Time'], format='%H:%M:%S')
    
    # 'Time'을 인덱스로 설정
    filtered_df.set_index('Time', inplace=True)

    # 30분 단위로 리샘플링하여 RCPI 평균 계산
    rcpi_by_time_30min = filtered_df.resample('30T')['RCPI'].mean()

    # 결과 출력 (각 30분 구간별 RCPI 평균)
    print(rcpi_by_time_30min)

    # 그래프 시각화
    plt.figure(figsize=(10, 6))
    rcpi_by_time_30min.plot(kind='bar', color='skyblue')
    plt.title("Average RCPI by 30-Minute Intervals (Filtered by Latitude and Longitude)")
    plt.xlabel("Time (HH:MM)")
    plt.ylabel("Average RCPI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
