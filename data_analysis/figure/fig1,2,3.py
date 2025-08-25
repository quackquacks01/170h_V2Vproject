import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from haversine import haversine

# 1. CSV 불러오기
df = pd.read_csv('output1_4.csv')

# 2. Timestamp 변환
#df['Tx_Timestamp'] = pd.to_datetime(df['Tx_Timestamp'])
#df['Rx_Timestamp'] = pd.to_datetime(df['Rx_Timestamp'])

# 3. 차량 간 거리 확인 및 보정 (필요 시 직접 계산)
def calc_distance(row):
    tx = (row['Tla'], row['Tlo'])
    rx = (row['Rla'], row['Rlo'])
    return haversine(tx, rx) * 1000  # m 단위

if 'Distance' not in df.columns or df['Distance'].isnull().any():
    df['Distance'] = df.apply(calc_distance, axis=1)

# ---------- 분석 시작 ----------

## 그림 1 RCPI 값 전체 분포 히스토그램
plt.figure(figsize=(8, 4))
plt.hist(df['RCPI'], bins=30, color='lightcoral', edgecolor='black')
plt.title('RCPI Value Histogram')
plt.xlabel('RCPI (dBm)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()

## 그림 2 차량 간 거리 분포 히스토그램 
plt.figure(figsize=(8, 4))
plt.hist(df['Distance'], bins=30, color='skyblue', edgecolor='black')
plt.title('Vehicle-to-Vehicle Distance Histogram')
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.show()

## 그림 3 거리 vs RCPI 산점도 (전체 거리 기준)
plt.figure(figsize=(6, 6))
sns.scatterplot(x='Distance', y='RCPI', data=df, alpha=0.6)
plt.title('Distance vs RCPI Scatter Plot')
plt.xlabel('Distance (m)')
plt.ylabel('RCPI (dBm)')
plt.grid(True)

# 상관계수 추가
r, p = pearsonr(df['Distance'], df['RCPI'])
plt.text(0.05, 0.95, f'Pearson r = {r:.2f}', transform=plt.gca().transAxes, fontsize=12, color='blue')
plt.tight_layout()
plt.show()