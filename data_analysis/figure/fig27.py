import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
df = pd.read_csv('rcpi_speed.csv')  # 파일명 필요시 수정

# 조건 필터링
filtered = df[
    (df['Speed(km/h)'] <= 1.0) &     # 속도가 거의 0인 경우
    (df['RCPI'] >= 100) &
    (df['RCPI'] <= 150)
]

# 히스토그램 시각화
plt.figure(figsize=(10, 5))
plt.hist(filtered['DistanceDelta(m)'], bins=30, color='teal', edgecolor='black')
plt.title("Histogram of Distance (Speed ≈ 0, RCPI 100~150, 5m Bins)")
plt.xlabel("Distance (m)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()