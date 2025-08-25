# 170h_V2Vproject 🚗📡

**실도로 기반 5G-V2X 통신 품질 이상 탐지 및 시각화 시스템**  
인하대학교 전기전자공학부 졸업논문 연구를 기반으로 한 프로젝트입니다.

---

## 📑 프로젝트 개요
- **실험 환경**: 판교 제로시티 도심 실도로, 28개 OBU 탑재 차량(4대), 170시간 이상 주행 로그 수집
- **데이터 종류**: RCPI(신호세기), Latency(지연시간), 속도, 거리, GPS
- **핵심 목표**  
  1. 실도로 기반 V2X 통신 품질 이상 현상 정량 분석  
  2. 반복 이상치(outlier) 탐지 및 제거 → 품질 안정성 향상  
  3. Streamlit 기반 실시간 시각화 대시보드 및 PDF 리포트 자동 생성  

---

## 📂 Repository 구조
```markdown
170h_V2Vproject/
│
├── data_analysis/ # 데이터 분석 및 전처리
│ ├── figure/ # 분석 결과 그래프/히트맵
│ ├── log_to_csv/ # 로그 → CSV 변환 스크립트
│ ├── output1_4.csv # 원본 데이터
│ ├── output1_4_removed_fixed_spot.csv # 이상치 제거 후 데이터
│ └── rcpi_speed.csv # 속도 기반 RCPI 분석 데이터
│
├── vehicle_map_project/ # 지도 기반 시각화
│ ├── vehicle_animation.py # 차량 주행 애니메이션
│ ├── sender_car.png # 송신 차량 아이콘
│ └── receiver_car.png # 수신 차량 아이콘
│
└── README.md
```

---

## ⚙️ 주요 기능
- **데이터 전처리**: JSON 로그 → CSV 변환, 시간 동기화, 거리/속도 계산
- **이상치 탐지/제거**  
  - RCPI < 80 dBm 또는 > 160 dBm  
  - 속도 ≤ 10km/h ∧ RCPI ≤ 100 dBm  
  - 속도 ≥ 60km/h ∧ RCPI ≥ 130 dBm
- **통계 분석 & 시각화**  
  - RCPI–거리/속도 상관 분석
  - Latency 분포 (평균 5.38ms)
  - 공간 히트맵 기반 저품질 구간 분석
- **Streamlit 대시보드**  
  - 지도 기반 통신 품질 애니메이션
  - 조건별 필터링 (RCPI/Latency/구간별)
  - PDF 리포트 자동 생성

---

## 🏆 주요 성과
- 170시간 실도로 주행 로그 기반의 **대규모 실증 데이터 분석**
- 반복 이상치 제거로 통신 품질 예측 정확도 **+14.2% 향상**
- **터널 음영 구간 개선안 제시** (RF 증폭기 설치 방안)
- Streamlit 기반 **실시간 시각화 대시보드** 및 **보고서 자동화 시스템** 구현
- 한국통신학회 논문 제출 준비 중

---

## 🔧 기술 스택
- **언어**: Python (pandas, matplotlib, seaborn)
- **시각화**: Streamlit, Folium, pydeck
- **리포트 자동화**: ReportLab
- **데이터 처리**: GPS/Haversine 기반 거리 계산, 이상치 필터링

---

## 🚀 실행 방법
```bash
# 데이터 분석 실행
python data_analysis/log_to_csv/...

# 시각화 대시보드 실행
streamlit run vehicle_map_project/vehicle_animation.py
```

---

## 📜 License
MIT License Copyright (c) 2025 quackquacks01 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
