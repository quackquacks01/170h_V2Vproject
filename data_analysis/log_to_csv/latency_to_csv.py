'''
따로 추출하여 기존 csv에 복붙하는 형식으로 만듦
'''

import os
import csv

log_folder = r"C:\log_folder"
output_csv = r"C:\log_folder\latency1.csv"

results = []

for filename in os.listdir(log_folder):
    if filename.endswith(".log"):
        filepath = os.path.join(log_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            idx = 0

            while idx < len(lines):
                line = lines[idx]
                if 'Package : 4' in line:
                    # Timestamp for package 4
                    for i in range(idx, min(idx + 10, len(lines))):
                        if 'Timestamp -' in lines[i]:
                            ts4 = int(lines[i].split('Timestamp -')[1].strip())
                            break
                    # Timestamp for package 5
                    for j in range(i, min(i + 10, len(lines))):
                        if 'Package : 5' in lines[j]:
                            for k in range(j, min(j + 10, len(lines))):
                                if 'Timestamp -' in lines[k]:
                                    ts5 = int(lines[k].split('Timestamp -')[1].strip())
                                    latency = round((ts5 - ts4) * 1e-3, 1)  # 소수 첫째자리
                                    results.append([filename, latency])
                                    idx = k  # 다음 탐색 위치
                                    break
                            break
                idx += 1

# CSV 저장
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Filename', 'Latency (ms)'])
    writer.writerows(results)

print(f"결과 저장: {output_csv}")
