# 코드 치트시트 (세션 01~10 + 종합 패턴)

> 시험 중 다른 탭에서 열어 복붙용으로 쓰세요. 파일명·컬럼명은 **문제 지문대로 바꾸세요**. 대부분의 스니펫은 공식 실습 데이터로 실행 확인했습니다(YOLO/OCR은 환경 의존이라 미실행).

> ⚠ **시험 환경은 Python 3.9 + pandas 1.x 로 보입니다**(사전 테스트 오류 메시지 기준). 그래서 `root_mean_squared_error`(sklearn 1.4+)나 `resample("h")`(소문자, pandas 2.2+)는 쓰지 말고 이 문서의 방식을 쓰세요. 막히면 `pd.__version__`, `sklearn.__version__`으로 버전을 먼저 확인하세요.
>
> ⚠ **컬럼명은 지문과 실제 파일이 다를 수 있습니다**(예: 지문 `run_time_2km(sec)` ↔ 실제 파일 `run_time_2km`). 항상 `df.columns`로 먼저 확인하세요.


## 0. 공통 시작

### 기본 import & 파일 입출력 (형식 예시, 실행용 아님)
```python
import os, numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
df = pd.read_csv("data.csv")            # 한글 깨지면 encoding="cp949"
df.head(); df.info(); df.describe(); df.isna().sum(); df.shape
df.to_csv("result.csv", index=False)    # index=False 필수
os.makedirs("plots", exist_ok=True)
```


## 01 결측·이상치

### 결측치 대치
```python
df = pd.read_csv("maintenance_log.csv")
df["repair_count"] = df["repair_count"].fillna(df["repair_count"].mean())
df["repair_duration"] = df["repair_duration"].fillna(df["repair_duration"].mean())
df["last_check_day"] = df["last_check_day"].fillna(df["last_check_day"].median())
df.to_csv("maintenance_cleaned.csv", index=False)
```

### 임시 컬럼은 저장 전에 삭제 (세션 01 주의점)
```python
# 계산용으로 내가 만든 컬럼은 저장 전에 지운다. 문제에서 요구한 컬럼이면 남긴다.
df["bmi_z"] = (df["bmi"] - df["bmi"].mean()) / df["bmi"].std(ddof=0)   # 임시 컬럼
df = df[df["bmi_z"].abs() <= 3]
df = df.drop(columns=["bmi_z"])                   # ← 저장 전 삭제
print(df.columns.tolist())                        # 원래 컬럼만 남았는지 확인
df.to_csv("health_clean.csv", index=False)
```

### Z-score 이상치 제거 / IQR
```python
df = pd.read_csv("health_check.csv")
cols = ["bmi", "blood_pressure"]
# scipy 없이 pandas만으로 Z-score (scipy.stats.zscore와 같은 값: ddof=0)
z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
# (scipy를 쓸 수 있다면: from scipy.stats import zscore; z = df[cols].apply(zscore))
mask = (z.abs() <= 3).all(axis=1)          # 둘 다 3 이하인 행만 남김
print("제거된 행 수:", (~mask).sum())
clean = df[mask]; clean.to_csv("health_clean.csv", index=False)

# IQR 방식
q1, q3 = df["bmi"].quantile([.25, .75]); iqr = q3 - q1
df_iqr = df[df["bmi"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]
```

### 센서 병합 + 'error' 처리
```python
m = pd.read_csv("motion_sensor.csv"); t = pd.read_csv("temp_sensor.csv")
merged = pd.merge(m, t, on=["time", "post_id"], how="inner")   # 기준 열은 지문에 맞게
merged["motion_count"] = pd.to_numeric(merged["motion_count"], errors="coerce")  # "error" → NaN
merged["motion_count"] = merged["motion_count"].fillna(merged["motion_count"].mean())
merged = merged.dropna()
merged.to_csv("merged_sensor_cleaned.csv", index=False)
```


## 02 정규화·인코딩

### MinMax 정규화 + 원본과 결합
```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler
df = pd.read_csv("fitness_test.csv")
cols = ["pushup_count", "run_time_2km", "situp_count"]     # 실제 컬럼명은 df.columns로 확인
scaled = pd.DataFrame(MinMaxScaler().fit_transform(df[cols]), columns=[c + "_scaled" for c in cols])
out = pd.concat([df, scaled], axis=1); out.to_csv("fitness_scaled.csv", index=False)
print(scaled.min(), scaled.max())       # StandardScaler는 평균0·표준편차1
```

### 라벨/원핫 인코딩
```python
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv("soldier_info.csv")
le = LabelEncoder(); df["position_enc"] = le.fit_transform(df["position"])
print(dict(zip(le.classes_, le.transform(le.classes_))))   # 인코딩 설명 출력
df = pd.get_dummies(df, columns=["region"], dtype=int)      # 원핫
df.to_csv("encoded_soldiers.csv", index=False)
```

### 파일 존재 여부 필터
```python
df = pd.read_csv("video_metadata.csv")
df["exists"] = df["file_path"].apply(lambda p: os.path.exists(p))
df[df["exists"]].to_csv("valid_videos.csv", index=False)
df[~df["exists"]].to_csv("missing_videos.csv", index=False)
```


## 03 시계열·JSON

### 시계열 정렬·리샘플링·시각화
```python
df = pd.read_csv("sensor_log.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").set_index("timestamp")
hourly = df["motion_detected"].resample("H").sum()     # 시험 환경(pandas 1.x)은 대문자 "H". 최신 pandas는 "h"
hourly.to_csv("hourly_motion.csv")
plt.figure(figsize=(10, 4)); plt.plot(hourly.index, hourly.values)
plt.title("Hourly motion"); plt.xlabel("time"); plt.ylabel("sum"); plt.grid(True)
plt.tight_layout(); plt.savefig("hourly_motion.png"); plt.close()
```

### JSON → DataFrame
```python
import json
with open("supply.json", encoding="utf-8") as f: data = json.load(f)
df = pd.json_normalize(data)
df = df.rename(columns={"items.water": "water", "items.ration": "ration", "items.medicine": "medicine"})
df.to_csv("supply_log.csv", index=False)
print(df[["water", "ration", "medicine"]].sum())
```


## 04 기술통계

### agg / groupby / 최빈값
```python
df = pd.read_csv("health_summary.csv")
cols = ["temperature", "pulse", "weight"]
overall = df[cols].agg(["mean", "median", "std"])
by_unit = df.groupby("unit")[cols].agg(["mean", "std"])
by_unit.columns = ["_".join(c) for c in by_unit.columns]       # 다중 컬럼 평탄화
overall.to_csv("health_stats.csv"); by_unit.to_csv("unit_stats.csv")
df[cols].mode().iloc[0]            # 최빈값 / df[cols].var(), .quantile([.25,.75])
```


## 05 시각화

### 히스토그램·박스플롯·산점도·heatmap
```python
df = pd.read_csv("fitness_result.csv"); cols = ["pushup_count", "run_time_2km(sec)", "situp_count"]
fig, ax = plt.subplots(2, 3, figsize=(14, 7))
for i, c in enumerate(cols):
    ax[0, i].hist(df[c], bins=15); ax[0, i].set_title(f"{c} hist")
    ax[1, i].boxplot(df[c]);      ax[1, i].set_title(f"{c} box")
plt.tight_layout(); os.makedirs("plots", exist_ok=True); plt.savefig("plots/dist.png"); plt.close()

s = pd.read_csv("stress_factors.csv")
sns.scatterplot(data=s, x="training_pressure", y="command_tension", hue="unit"); plt.savefig("scatter_plot.png"); plt.close()
sns.heatmap(s.select_dtypes("number").corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.tight_layout(); plt.savefig("stress_correlation.png"); plt.close()
```


## 06 해석

### 상관·그룹 비교·pivot_table
```python
df = pd.read_csv("stress_analysis.csv")
r = df["sleep_quality"].corr(df["training_pressure"]); print(round(r, 3))
th = df["command_tension"].median()                           # 임계치
hi = df[df["command_tension"] > th]["sleep_quality"].mean()
lo = df[df["command_tension"] <= th]["sleep_quality"].mean()
print(round(hi, 2), round(lo, 2))

m = pd.read_csv("meal_feedback.csv"); score = ["taste_score", "quantity_score", "cleanliness_score"]
avg = m.groupby("unit")[score].mean().round(2); avg.to_csv("meal_unit_avg.csv")
print(m[score].mean().idxmin())                                # 가장 낮은 항목명
pt = pd.pivot_table(m, index="unit", values=score, aggfunc="mean")
```


## 07 지도학습

### 분류 (RandomForest) + 평가
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
df = pd.read_csv("combat_ready.csv")
df["status_enc"] = (df["status"] == "적합").astype(int)       # 적합=1, 부적합=0 명시
X = df[["pushup_count", "run_time_2km(sec)", "sprint_100m(sec)"]]; y = df["status_enc"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(random_state=42).fit(Xtr, ytr); pred = clf.predict(Xte)
res = df.loc[Xte.index, ["soldier_id"]].copy(); res["actual"] = yte.values; res["pred"] = pred
res.to_csv("combat_ready_result.csv", index=False)
print(accuracy_score(yte, pred)); print(confusion_matrix(yte, pred)); print(classification_report(yte, pred))
```

### 회귀 (LinearRegression) + RMSE
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
df = pd.read_csv("equipment_life.csv")
X = df[["usage_hours", "temp_exposure", "humidity"]]; y = df["remaining_life_days"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
reg = LinearRegression().fit(Xtr, ytr); pred = reg.predict(Xte)
rmse = np.sqrt(mean_squared_error(yte, pred)); print(rmse, mean_absolute_error(yte, pred), r2_score(yte, pred))
pd.DataFrame({"equipment_id": df.loc[Xte.index, "equipment_id"], "predicted_life": pred}).to_csv("life_prediction.csv", index=False)
plt.scatter(yte, pred); plt.plot([yte.min(), yte.max()], [yte.min(), yte.max()], "r--")
plt.xlabel("actual"); plt.ylabel("predicted"); plt.savefig("life_plot.png"); plt.close()
```

### 다중분류 (A/B/C)
```python
from sklearn.ensemble import GradientBoostingClassifier
df = pd.read_csv("maintenance_priority.csv")
le = LabelEncoder(); y = le.fit_transform(df["priority_level"])    # A,B,C → 0,1,2
X = df[["age_years", "error_logs_per_month", "functional_score", "last_repair_months"]]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = GradientBoostingClassifier(random_state=42).fit(Xtr, ytr); p = m.predict(Xte)
print(classification_report(yte, p, target_names=le.classes_)); print(confusion_matrix(yte, p))
out = df.loc[Xte.index, ["weapon_id"]].copy(); out["predicted"] = le.inverse_transform(p)
out.to_csv("priority_prediction.csv", index=False)
```


## 08 비지도학습

### KMeans + PCA
```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
df = pd.read_csv("duty_pattern.csv"); feats = [c for c in df.columns if c != "soldier_id"]
X = StandardScaler().fit_transform(df[feats])
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X); df["cluster"] = km.labels_
print(silhouette_score(X, km.labels_)); print(df.groupby("cluster")[feats].mean())
print(df["cluster"].value_counts().sort_index())                  # 군집별 인원 (막대그래프용)
p = PCA(n_components=2).fit(X); Z = p.transform(X); print(p.explained_variance_ratio_, p.components_)
plt.scatter(Z[:, 0], Z[:, 1], c=df["cluster"], cmap="viridis"); plt.xlabel("PC1"); plt.ylabel("PC2")
plt.savefig("duty_pca_plot.png"); plt.close(); df.to_csv("duty_clusters.csv", index=False)
```


## 09 이미지(OpenCV)

### 리사이즈·그레이·밝기
```python
import cv2
rows = []
for f in sorted(os.listdir("images/night_ops")):
    if not f.lower().endswith((".png", ".jpg", ".jpeg")): continue
    img = cv2.imread(f"images/night_ops/{f}")            # BGR
    img = cv2.resize(img, (256, 256))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows.append({"filename": f, "brightness": gray.mean()})
b = pd.DataFrame(rows); b.to_csv("brightness_result.csv", index=False)
print(b.loc[b["brightness"].idxmax(), "filename"])
```

### 사각형 윤곽 검출
```python
rows = []
for f in sorted(os.listdir("images/blueprints")):
    img = cv2.imread(f"images/blueprints/{f}"); gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    n = 0
    for c in cnts:
        ap = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
        if len(ap) == 4 and cv2.isContourConvex(ap):
            x, y, w, h = cv2.boundingRect(ap); n += 1
            rows.append({"filename": f, "x": x, "y": y, "width": w, "height": h})
    print(f, "사각형 수:", n)
pd.DataFrame(rows).to_csv("rectangles.csv", index=False)
```

### YOLOv5(torch.hub) 탐지 → csv
```python
import torch
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)   # 인터넷 필요
rows = []
for f in sorted(os.listdir("images/surv_imgs")):
    img = cv2.imread(f"images/surv_imgs/{f}")[:, :, ::-1]                   # BGR → RGB
    d = model(img).pandas().xyxy[0]                                          # xmin,ymin,xmax,ymax,confidence,class,name
    for _, r in d.iterrows():
        rows.append({"filename": f, "class": r["name"], "x1": r.xmin, "y1": r.ymin, "x2": r.xmax, "y2": r.ymax})
det = pd.DataFrame(rows); det.to_csv("detections.csv", index=False)
print((det["class"] == "person").sum(), det["class"].isin(["car", "truck", "bus"]).sum())
```

### YOLOv8(ultralytics) 대안 — torch.hub가 막힐 때
```python
# pip install ultralytics
from ultralytics import YOLO
model = YOLO("yolov8n.pt")            # 가중치 다운로드 필요
r = model.predict("img.png", device="cpu", verbose=False)[0]
for (x1, y1, x2, y2), c in zip(r.boxes.xyxy.tolist(), r.boxes.cls.tolist()):
    print(r.names[int(c)], x1, y1, x2, y2)            # COCO: person=0, car=2, bus=5, truck=7
```


## 10 이미지 분류·OCR·영상

### 클래스 빈도 + Top3 막대그래프
```python
from collections import Counter
cnt = Counter(det["class"])                         # 위에서 만든 detections 사용
pd.DataFrame(cnt.items(), columns=["class", "count"]).sort_values("count", ascending=False).to_csv("object_count.csv", index=False)
top3 = cnt.most_common(3)
plt.bar([k for k, _ in top3], [v for _, v in top3]); plt.title("Top3 objects"); plt.savefig("top3_objects.png"); plt.close()
```

### EasyOCR + 정규식
```python
import easyocr, re
reader = easyocr.Reader(["ko", "en"], gpu=False)     # 첫 실행 시 모델 다운로드
rows = []
for f in sorted(os.listdir("images/supplies_imgs")):
    for bbox, text, conf in reader.readtext(f"images/supplies_imgs/{f}"):
        if re.match(r"^[가-힣A-Za-z0-9\s]+$", text):          # 한글·영문·숫자만
            rows.append({"filename": f, "text": text, "conf": round(conf, 3)})
pd.DataFrame(rows).to_csv("supply_info.csv", index=False)
```

### 영상 프레임 추출 (1초 간격)
```python
cap = cv2.VideoCapture("videos/drone_mission.mp4")
assert cap.isOpened(), "영상을 열 수 없음"
fps = int(round(cap.get(cv2.CAP_PROP_FPS))) or 30
i, frames = 0, []
while True:
    ok, frame = cap.read()
    if not ok: break
    if i % fps == 0: frames.append((i, frame))        # frame_number, 이미지
    i += 1
cap.release(); print(len(frames), "프레임 추출")
# frames 각각에 YOLO 적용 → frame_number,class,x1,y1,x2,y2 저장 → 프레임별 개수 plot
```


## 공통 패턴

### 종합문제 레시피 (표 데이터)
```python
# 회귀: 정규화 → 분할 → RandomForestRegressor → RMSE → 예측 csv → 그래프
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error             # 구버전 sklearn에서도 되는 방식
X = StandardScaler().fit_transform(df[feats]); y = df[target]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = RandomForestRegressor(random_state=42).fit(Xtr, ytr); p = m.predict(Xte); print(np.sqrt(mean_squared_error(yte, p)))   # RMSE
imp = pd.Series(m.feature_importances_, index=feats).sort_values(ascending=False)   # 변수 중요도
# 이상탐지: IsolationForest(contamination=0.05).fit_predict(X) == -1 → anomaly=1
```
