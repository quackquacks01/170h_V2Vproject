import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 파일 불러오기
df = pd.read_csv('output1_4.csv')  # 파일 경로는 실제 위치에 맞게 수정

# 2. 위경도 정규화 (선택 사항: 시각화에는 직접적 영향 없음)
df['Latitude'] = df['Rla'] / 1e7
df['Longitude'] = df['Rlo'] / 1e7

# 3. RCPI 범위 필터링: 80 이상 160 이하만 사용
df_clean = df[(df['RCPI'] >= 80) & (df['RCPI'] <= 160)]

# 4. 거리 제한: 0~100m 사이만 시각화 대상으로 사용
df_plot = df_clean[df_clean['Distance'] <= 100]

# 5. 산점도 시각화
plt.figure(figsize=(10, 6))
plt.scatter(df_plot['Distance'], df_plot['RCPI'], color='mediumseagreen', alpha=0.3)
plt.title("Distance vs RCPI (0–100m, Cleaned)")
plt.xlabel("Distance (m)")
plt.ylabel("RCPI (dBm)")
plt.ylim(60, 180)
plt.grid(True)
plt.tight_layout()
plt.show()
