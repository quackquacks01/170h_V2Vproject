'''
package에서 정리하고 싶은 레이블 추출
package 4, 5 각각 반복
'''

import os
import re
import pandas as pd

def extract_data_from_log(file_path):
    pattern = re.compile(
        r"\[(?P<time>\d{2}:\d{2}:\d{2})\]\s+Package\s+:\s+(?P<package>\d+).*?"
        r"Latitude\s+-\s+(?P<latitude>\d+),\s+Longitude\s+-\s+(?P<longitude>\d+).*?"
        r"RSSI\s+-\s+(?P<rssi>-?\d+),\s+RCPI\s+-\s+(?P<rcpi>\d+)",
        re.DOTALL
    )
    with open(file_path, 'r') as f:
        text = f.read()
    matches = pattern.finditer(text)
    return [
        {
            "Time": m.group("time"),
            "Package": m.group("package"),
            "Latitude": m.group("latitude"),
            "Longitude": m.group("longitude"),
            "RSSI": m.group("rssi"),
            "RCPI": m.group("rcpi"),
        }
        for m in matches
    ]

log_folder_path = "C:\log_folder"

all_data = []

for file in os.listdir(log_folder_path):  # Replace with your log folder path
    if file.endswith(".log"):  # or .pdf after extracting text
        all_data.extend(extract_data_from_log(os.path.join(log_folder_path, file)))

df = pd.DataFrame(all_data)
df.to_csv("output0.csv", index=False)
