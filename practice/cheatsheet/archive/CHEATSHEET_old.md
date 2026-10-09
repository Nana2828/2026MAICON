# 코드 치트시트 (세션 01~10 + 종합 패턴)

> 시험 중 다른 탭에서 열어 복붙용으로 쓰세요. 파일명·컬럼명은 **문제 지문대로 바꾸세요**. 대부분의 스니펫은 공식 실습 데이터로 실행 확인했습니다(YOLO/OCR은 환경 의존이라 미실행).

> ⚠ **시험 환경은 Python 3.9 + pandas 1.x 로 보입니다**(사전 테스트 오류 메시지 기준). 그래서 `root_mean_squared_error`(sklearn 1.4+)나 `resample("h")`(소문자, pandas 2.2+)는 쓰지 말고 이 문서의 방식을 쓰세요. 막히면 `pd.__version__`, `sklearn.__version__`으로 버전을 먼저 확인하세요.
>
> ⚠ **컬럼명은 지문과 실제 파일이 다를 수 있습니다**(예: 지문 `run_time_2km(sec)` ↔ 실제 파일 `run_time_2km`). 항상 `df.columns`로 먼저 확인하세요.


## 🧭 어떤 걸 써야 하나? (문제 유형 → 선택 가이드)

지문의 **키워드**를 보고 아래에서 고르세요. 자세한 코드는 해당 섹션을 보세요.

| 지문에 이런 말이 있으면 | 이렇게 한다 |
|---|---|
| 빈칸 / 누락 / NaN | `fillna(평균·중앙값)` 또는 `dropna()` — 지문이 정한 방식 그대로 |
| 이상치 제거·탐지 | Z-score(3 초과) 또는 IQR(1.5배) — 지문이 정한 방식 |
| 합쳐라 / 통합 | `pd.merge(on=기준열)` (행을 이어붙이면 `pd.concat`) |
| 정규화(0~1) / 표준화 | MinMaxScaler / StandardScaler |
| 문자 → 숫자 | 정답열·순서 있음 = LabelEncoder, 입력 특성(순서 없음) = `get_dummies` |
| 시간/일/주 단위 집계 | `to_datetime` → 정렬 → `resample` |
| JSON | `json.load` → `json_normalize` → `rename` |
| 평균·중앙값·표준편차 | `agg` (그룹별이면 `groupby`) |
| 분포 / 이상치 그래프 | 히스토그램 / 박스플롯 |
| 두 변수 관계 / 상관 | 산점도 / `corr` + heatmap |
| ~별 평균, 표로 요약 | `groupby().mean()` / `pivot_table` |
| 정답이 **범주**(적합·부적합, A/B/C) | 분류: RandomForestClassifier 등 → 정확도·혼동행렬 |
| 정답이 **숫자**(수명·점수) | 회귀: LinearRegression/RandomForestRegressor → RMSE |
| 비슷한 것끼리 묶기(정답 없음) | KMeans (먼저 표준화) |
| 2차원으로 줄여 시각화 | PCA (먼저 표준화) |
| 이상 탐지 | IsolationForest (contamination 지정) |
| 사람/차량 탐지, 개수 | YOLO → 클래스별 집계 |
| 이미지 속 글자 | EasyOCR + 정규식 |
| 사각형·윤곽 | Canny → findContours → approxPolyDP |
| 영상 프레임 | VideoCapture 루프, `i % fps == 0` |

**공통 체크**: 파일명·컬럼명을 지문과 한 글자도 다르지 않게 / 모델은 `train_test_split` 후 **테스트셋으로 평가** / 임시 컬럼 삭제 / `index=False`로 저장.

## 0. 공통 시작

### 기본 import & 파일 입출력 (형식 예시, 실행용 아님)

> **언제 쓰나**: 모든 문제의 시작. 파일을 읽을 땐 `read_csv`, 결과 저장은 반드시 `to_csv(index=False)`. 한글 깨지면 `encoding='cp949'`.

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

> **언제 쓰나**: 지문에 "빈칸/누락/NaN을 채워라"가 있을 때. **평균**은 값이 고르게 퍼진 열, **중앙값**은 극단값(이상치)이 섞인 열, 지문이 지정하면 그대로 따른다. 행을 버리라고 하면 `dropna()`.

```python
df = pd.read_csv("maintenance_log.csv")
df["repair_count"] = df["repair_count"].fillna(df["repair_count"].mean())   # 평균: 지문이 "평균으로" 라고 할 때
df["repair_duration"] = df["repair_duration"].fillna(df["repair_duration"].mean())
df["last_check_day"] = df["last_check_day"].fillna(df["last_check_day"].median())   # 중앙값: 지문이 "중앙값으로"일 때(극단값에 강함)
df.to_csv("maintenance_cleaned.csv", index=False)
```

### 임시 컬럼은 저장 전에 삭제 (세션 01 주의점)

> **언제 쓰나**: 계산하려고 내가 만든 컬럼(z값, 플래그 등)이 있을 때. 저장 직전에 `drop`으로 지운다. 지문이 그 컬럼을 요구했으면 남긴다.

```python
# 계산용으로 내가 만든 컬럼은 저장 전에 지운다. 문제에서 요구한 컬럼이면 남긴다.
df["bmi_z"] = (df["bmi"] - df["bmi"].mean()) / df["bmi"].std(ddof=0)   # 임시 컬럼
df = df[df["bmi_z"].abs() <= 3]
df = df.drop(columns=["bmi_z"])                   # ← 저장 전 삭제
print(df.columns.tolist())                        # 원래 컬럼만 남았는지 확인
df.to_csv("health_clean.csv", index=False)
```

### Z-score 이상치 제거 / IQR

> **언제 쓰나**: "이상치를 제거/탐지하라"일 때. 지문이 **Z-score 3**이라 하면 Z-score, **IQR/사분위**라 하면 IQR. 정규분포에 가까우면 Z-score, 치우친 분포·극단값이 많으면 IQR.

```python
df = pd.read_csv("health_check.csv")
cols = ["bmi", "blood_pressure"]
# scipy 없이 pandas만으로 Z-score (scipy.stats.zscore와 같은 값: ddof=0)
z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
# (scipy를 쓸 수 있다면: from scipy.stats import zscore; z = df[cols].apply(zscore))
mask = (z.abs() <= 3).all(axis=1)          # Z-score 3 초과를 이상치로 보라는 지문일 때. 여러 열이면 .all(axis=1)로 모두 정상인 행만 남김
print("제거된 행 수:", (~mask).sum())
clean = df[mask]; clean.to_csv("health_clean.csv", index=False)

# IQR 방식
q1, q3 = df["bmi"].quantile([.25, .75]); iqr = q3 - q1
df_iqr = df[df["bmi"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]   # IQR/사분위 방식으로 하라는 지문일 때
```

### 센서 병합 + 'error' 처리

> **언제 쓰나**: 파일이 여러 개이고 "합쳐라/통합하라"일 때 `merge`(기준 열 지정). 숫자 열에 `'error'` 같은 문자가 섞이면 `to_numeric(errors='coerce')`로 NaN 처리 후 채우기/삭제.

```python
m = pd.read_csv("motion_sensor.csv"); t = pd.read_csv("temp_sensor.csv")
merged = pd.merge(m, t, on=["time", "post_id"], how="inner")   # inner=양쪽에 다 있는 행만 / left=왼쪽 표 기준 유지. 지문에 맞게
merged["motion_count"] = pd.to_numeric(merged["motion_count"], errors="coerce")  # "error" → NaN
merged["motion_count"] = merged["motion_count"].fillna(merged["motion_count"].mean())
merged = merged.dropna()
merged.to_csv("merged_sensor_cleaned.csv", index=False)
```


## 02 정규화·인코딩

### MinMax 정규화 + 원본과 결합

> **언제 쓰나**: 지문이 **"0~1 정규화"**이면 MinMaxScaler, **"표준화(평균0·표준편차1)"**이면 StandardScaler. 거리 기반 모델(KMeans, PCA)이나 단위가 다른 열을 비교할 때 사용.

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler
df = pd.read_csv("fitness_test.csv")
cols = ["pushup_count", "run_time_2km", "situp_count"]     # 실제 컬럼명은 df.columns로 확인
scaled = pd.DataFrame(MinMaxScaler().fit_transform(df[cols]), columns=[c + "_scaled" for c in cols])
out = pd.concat([df, scaled], axis=1); out.to_csv("fitness_scaled.csv", index=False)
print(scaled.min(), scaled.max())       # StandardScaler는 평균0·표준편차1
```

### 라벨/원핫 인코딩

> **언제 쓰나**: 문자(범주) 열을 모델/계산에 쓸 때. 순서가 의미 있거나 클래스가 2개·타깃(정답) 열이면 **라벨 인코딩**, 순서가 없는 입력 특성(지역, 보직 등)은 **원핫(get_dummies)**.

```python
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv("soldier_info.csv")
le = LabelEncoder(); df["position_enc"] = le.fit_transform(df["position"])
print(dict(zip(le.classes_, le.transform(le.classes_))))   # 인코딩 설명 출력
df = pd.get_dummies(df, columns=["region"], dtype=int)      # 원핫: 순서 없는 범주(지역 등). 라벨 인코딩은 정답열/순서 있는 범주
df.to_csv("encoded_soldiers.csv", index=False)
```

### 파일 존재 여부 필터

> **언제 쓰나**: 표에 파일 경로가 있고 "실제 있는 것만 남겨라"일 때. `apply(os.path.exists)`로 True/False 열을 만든 뒤 필터링.

```python
df = pd.read_csv("video_metadata.csv")
df["exists"] = df["file_path"].apply(lambda p: os.path.exists(p))
df[df["exists"]].to_csv("valid_videos.csv", index=False)
df[~df["exists"]].to_csv("missing_videos.csv", index=False)
```


## 03 시계열·JSON

### 시계열 정렬·리샘플링·시각화

> **언제 쓰나**: 시간 컬럼이 있고 "시간/일/주 단위로 합계·평균을 내라"일 때. 반드시 `to_datetime` → 정렬/인덱스 → `resample`. 주기: 분 `min`, 시간 `H`, 일 `D`, 주 `W`, 월 `M`.

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

> **언제 쓰나**: 입력이 `.json`이거나 한 칸 안에 딕셔너리가 중첩(`items`)되어 있을 때. 중첩이면 `json_normalize`, 컬럼명은 `rename`으로 정리.

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

> **언제 쓰나**: "평균·중앙값·표준편차를 구하라"는 `agg`, "부대별/유형별로"가 붙으면 `groupby` 후 `agg`. 점수처럼 이산값의 대표값은 `mode()`.

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

> **언제 쓰나**: 분포를 볼 때 **히스토그램**, 이상치를 볼 때 **박스플롯**, 두 변수 관계는 **산점도**, 여러 변수 상관은 **corr + heatmap**. 저장은 `savefig` 후 `close()`.

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

> **언제 쓰나**: "관계/영향을 해석하라"는 상관계수(`corr`), "그룹 간 비교"는 `groupby().mean()`, "표로 요약/구조화하라"는 `pivot_table`. 해석은 숫자 근거 + 한두 문장.

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

> **언제 쓰나**: 정답(타깃)이 **범주**(적합/부적합, A/B/C)일 때. 평가는 정확도·혼동행렬·classification_report. 불균형이면 정확도만 보지 말고 report의 F1을 본다.

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

> **언제 쓰나**: 정답(타깃)이 **숫자**(수명, 점수)일 때. 지문이 모델을 지정하면 그것을 쓰고, 안 하면 `RandomForestRegressor`가 무난. 평가는 RMSE(작을수록 좋음).

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

> **언제 쓰나**: 타깃 클래스가 3개 이상일 때. 문자 라벨은 `LabelEncoder`로 숫자로 바꾸고, 결과는 `inverse_transform`으로 되돌려 저장.

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

> **언제 쓰나**: **정답 없이** 비슷한 것끼리 묶으라(군집)면 KMeans, 많은 열을 2차원으로 줄여 시각화하라면 PCA. 둘 다 먼저 `StandardScaler`로 표준화.

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

> **언제 쓰나**: "이미지 크기 통일/흑백/밝기"일 때. `imread`는 BGR이라 흑백은 `COLOR_BGR2GRAY`. 폴더의 이미지를 `listdir`로 순회.

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

> **언제 쓰나**: "도형/윤곽/사각형 좌표"일 때. Blur → Canny → findContours → approxPolyDP로 꼭짓점이 4개인 것만 → boundingRect.

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

> **언제 쓰나**: "사람/차량 같은 **객체 탐지**"일 때. 결과 표(`xyxy[0]`)의 `name`으로 클래스를 세고 좌표를 csv로 저장. 인터넷이 막히면 YOLOv8 방식 사용.

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

> **언제 쓰나**: `torch.hub.load`가 안 될 때. `pip install ultralytics` 후 `YOLO('yolov8n.pt')`. 가장 작은 모델(n)이 CPU에서 빠름.

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

> **언제 쓰나**: "탐지된 객체의 빈도/상위 N개"일 때 `Counter`(`most_common(N)`) 후 막대그래프.

```python
from collections import Counter
cnt = Counter(det["class"])                         # 위에서 만든 detections 사용
pd.DataFrame(cnt.items(), columns=["class", "count"]).sort_values("count", ascending=False).to_csv("object_count.csv", index=False)
top3 = cnt.most_common(3)
plt.bar([k for k, _ in top3], [v for _, v in top3]); plt.title("Top3 objects"); plt.savefig("top3_objects.png"); plt.close()
```

### EasyOCR + 정규식

> **언제 쓰나**: 이미지 속 **글자를 읽어라(OCR)**일 때. `Reader(['ko','en'])` + `readtext`, 특수문자 걸러내라면 정규식 `re.match`.

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

> **언제 쓰나**: 영상(`.mp4`)을 "프레임 단위로 분석/일정 간격 추출"일 때. `VideoCapture` 루프에서 `i % fps == 0`인 프레임만 처리.

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

> **언제 쓰나**: 종합 문제의 표 데이터 예측: **정규화 → 분할 → 모델 → 평가 → 결과 csv → 그래프**. 변수 영향도를 물으면 `feature_importances_`, 이상 탐지는 `IsolationForest`.

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
