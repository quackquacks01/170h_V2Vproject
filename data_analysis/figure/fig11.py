import pandas as pd
import matplotlib.pyplot as plt

# CSV 불러오기
df = pd.read_csv('rcpi_speed.csv')  # 파일 경로 필요 시 수정

# 기본 조건: Δt ≥ 0.1, Speed ≤ 120, RCPI 80~160
filtered = df[(df['TimeDelta(s)'] >= 0.1) & (df['Speed(km/h)'] <= 120)]
filtered_clean = filtered[(filtered['RCPI'] >= 80) & (filtered['RCPI'] <= 160)]

# 1차 이상치 제거: RCPI > 160 & Speed > 100
filtered_strict = filtered_clean[~(
    (filtered_clean['RCPI'] > 160) & (filtered_clean['Speed(km/h)'] > 100)
)]

# 2차 이상치 제거:
# - 고속에서 RCPI 너무 높은 경우 (Speed > 80 & RCPI > 130)
# - 저속에서 RCPI 너무 낮은 경우 (Speed < 5 & RCPI < 100)
final_filtered = filtered_strict[~(
    ((filtered_strict['Speed(km/h)'] > 80) & (filtered_strict['RCPI'] > 130)) |
    ((filtered_strict['Speed(km/h)'] < 5) & (filtered_strict['RCPI'] < 100))
)]

# 그래프 그리기
plt.figure(figsize=(8, 5))
plt.scatter(final_filtered['Speed(km/h)'], final_filtered['RCPI'], color='green', alpha=0.4)
plt.xlabel("Speed from TX (km/h)")
plt.ylabel("RCPI (dBm)")
plt.title("Speed vs RCPI (0–120 km/h), Final Cleaned: RCPI 80–160, All Outliers Removed")
plt.ylim(60, 180)
plt.grid(True)
plt.tight_layout()
plt.show()
