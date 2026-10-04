# 📚 세션별 학습 가이드 (개념 → 문제 → 함수 → 코드)

> 수업 PPT 순서 그대로, **세션마다**  
> ① 개념 → ② 문제별 지문 요점 → ③ PPT '활용 코드 정리' 함수(뜻·언제) → ④ 복붙 코드  
> 순서로 이어 놨습니다. 시험 중에는 **지문의 번호 [1][2][3]을 보고 해당 세션·문제로 가서 코드를 가져오면** 됩니다.

> ⚠ 시험 환경은 Python 3.9 + pandas 1.x로 보입니다(RMSE는 `np.sqrt(mean_squared_error)`, 리샘플링은 `"H"`). 컬럼명은 지문과 실제 파일이 다를 수 있으니 `df.columns`로 확인하세요.
> ⚠ **임시로 만든 컬럼은 저장 전에 삭제**(문제에서 요구했으면 유지), 저장은 `index=False`, 파일명은 지문과 한 글자도 다르지 않게.

## 목차
- [세션 01. 결측치·이상치 처리](#세션-01-결측치·이상치-처리)
- [세션 02. 정규화·인코딩](#세션-02-정규화·인코딩)
- [세션 03. 시계열 정렬·리샘플링 / JSON](#세션-03-시계열-정렬·리샘플링-/-JSON)
- [세션 04. 기술통계량](#세션-04-기술통계량)
- [세션 05. 데이터 시각화](#세션-05-데이터-시각화)
- [세션 06. 데이터 해석](#세션-06-데이터-해석)
- [세션 07. 지도학습 및 평가](#세션-07-지도학습-및-평가)
- [세션 08. 비지도학습](#세션-08-비지도학습)
- [세션 09. 이미지 처리 (OpenCV)](#세션-09-이미지-처리-(OpenCV))
- [세션 10. 이미지 분류·OCR·영상](#세션-10-이미지-분류·OCR·영상)


---

## 세션 01. 결측치·이상치 처리

### 📘 개념

**데이터 전처리란**: 분석에 적합한 형태로 데이터를 가공하는 것. 정리·변환 → 필요한 데이터 선택·통합 → 분석용 데이터셋 생성.
(구성: 결측치·이상치 처리 / 카테고리 인코딩 / 정규화·표준화)

**결측치 처리**: 수집 과정에서 누락된 값.
| 방법 | 내용 |
|---|---|
| 삭제 | 결측값이 있는 관측치(행)를 제거 |
| 평균대치법 | 해당 변수의 평균값으로 대체 |
| 단순확률대치법 | 변수의 분포에 따라 무작위로 대체 |
| 다중대치법 | 여러 번 대체해서 불확실성을 반영 |

**이상치**: 데이터 분포에서 멀리 떨어진 값.
| 방법 | 내용 |
|---|---|
| 표준편차(Z-변환) | 평균 ±3 표준편차를 벗어나면 이상값. Z-변환은 평균 0, 표준편차 1로 변환 |
| 사분위 범위(IQR) | IQR = Q3 − Q1, 하한 = Q1 − 1.5·IQR, 상한 = Q3 + 1.5·IQR |

### ✏ 문제 1. 정비 기록 결측치 처리

**지문 요점**
1. `repair_count`, `repair_duration` 빈칸 → 각 열의 **평균**으로
2. `last_check_day` 빈칸 → **중앙값**으로
3. `maintenance_cleaned.csv`로 저장

**활용 함수 (PPT '활용 코드 정리')**

- `pd.read_csv() / df.to_csv()` — 파일 읽기 / 저장  
  ↳ **언제**: 파일을 열 때 / 결과를 낼 때. 저장은 항상 `index=False`.
- `df.head() / df.describe()` — 앞 5줄 / 숫자 열 요약통계  
  ↳ **언제**: 데이터를 처음 볼 때(열 이름, 값 범위, 이상한 값 확인).
- `df['컬럼']` — 열 하나 고르기(Series)  
  ↳ **언제**: 열 하나만 계산·수정할 때. 여러 열은 `df[['a','b']]`(대괄호 2개).
- `fillna(값)` — 빈칸 채우기  
  ↳ **언제**: "빈칸을 ~로 채워라". 값은 평균/중앙값/0/최빈값 중 지문이 정한 것.
- `Series.mean() / median() / std()` — 평균 / 중앙값 / 표준편차  
  ↳ **언제**: 평균은 보통 값, 중앙값은 극단값이 있을 때, 표준편차는 흩어진 정도.

**코드**

> **언제 쓰나**: 지문에 "빈칸/누락/NaN을 채워라"가 있을 때. **평균**은 값이 고르게 퍼진 열, **중앙값**은 극단값(이상치)이 섞인 열, 지문이 지정하면 그대로 따른다. 행을 버리라고 하면 `dropna()`.

```python
df = pd.read_csv("maintenance_log.csv")
df["repair_count"] = df["repair_count"].fillna(df["repair_count"].mean())   # 평균: 지문이 "평균으로" 라고 할 때
df["repair_duration"] = df["repair_duration"].fillna(df["repair_duration"].mean())
df["last_check_day"] = df["last_check_day"].fillna(df["last_check_day"].median())   # 중앙값: 지문이 "중앙값으로"일 때(극단값에 강함)
df.to_csv("maintenance_cleaned.csv", index=False)
```

### ✏ 문제 2. 건강검진 이상치 제거

**지문 요점**
1. `bmi`, `blood_pressure`에서 **Z-score 3 초과**를 이상치로 보고 제거
2. `health_clean.csv`로 저장
3. **제거된 행 수 출력**

**활용 함수 (PPT '활용 코드 정리')**

- `scipy.stats.zscore` — 표준점수(Z). 절댓값 3 초과=이상치  
  ↳ **언제**: "Z-score로 이상치". scipy가 안 되면 `(x-x.mean())/x.std(ddof=0)`.
- `df[조건식]` — 조건에 맞는 행만 선택  
  ↳ **언제**: "~인 행만 남겨라/골라라". 조건 여러 개는 `(a) & (b)`, `|`로 묶고 각각 괄호.
- `apply()` — 각 열/값에 함수 적용  
  ↳ **언제**: 각 열/값에 함수를 한꺼번에 적용할 때(예: 열마다 zscore).
- `drop()` — 행/열 삭제  
  ↳ **언제**: 열을 지울 때 `columns=[...]`, 행을 지울 때 `index=[...]`. 임시 컬럼 정리에 사용.

**코드**

> **언제 쓰나**: 계산하려고 내가 만든 컬럼(z값, 플래그 등)이 있을 때. 저장 직전에 `drop`으로 지운다. 지문이 그 컬럼을 요구했으면 남긴다.

```python
# 계산용으로 내가 만든 컬럼은 저장 전에 지운다. 문제에서 요구한 컬럼이면 남긴다.
df["bmi_z"] = (df["bmi"] - df["bmi"].mean()) / df["bmi"].std(ddof=0)   # 임시 컬럼
df = df[df["bmi_z"].abs() <= 3]
df = df.drop(columns=["bmi_z"])                   # ← 저장 전 삭제
print(df.columns.tolist())                        # 원래 컬럼만 남았는지 확인
df.to_csv("health_clean.csv", index=False)
```

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

### ✏ 문제 3. 센서 로그 통합·정제

**지문 요점**
1. 두 센서 파일을 **시간 기준으로 병합**
2. `motion_count`의 `"error"` → 결측 → 전체 **평균**으로 대체
3. 남은 결측 행 제거 후 `merged_sensor_cleaned.csv` 저장

**활용 함수 (PPT '활용 코드 정리')**

- `pd.merge(a, b, on=, suffixes=)` — 두 표를 기준 열로 합치기. 겹치는 열 이름 구분  
  ↳ **언제**: 파일/표가 두 개 이상이고 "합쳐라". 기준 열이 같아야 하고 겹치는 열은 `suffixes`로 구분.
- `dropna()` — 빈칸이 있는 행 삭제  
  ↳ **언제**: "빈칸 있는 행은 제거". 특정 열만 보려면 `subset=[...]`.

**코드**

> **언제 쓰나**: 파일이 여러 개이고 "합쳐라/통합하라"일 때 `merge`(기준 열 지정). 숫자 열에 `'error'` 같은 문자가 섞이면 `to_numeric(errors='coerce')`로 NaN 처리 후 채우기/삭제.

```python
m = pd.read_csv("motion_sensor.csv"); t = pd.read_csv("temp_sensor.csv")
merged = pd.merge(m, t, on=["time", "post_id"], how="inner")   # inner=양쪽에 다 있는 행만 / left=왼쪽 표 기준 유지. 지문에 맞게
merged["motion_count"] = pd.to_numeric(merged["motion_count"], errors="coerce")  # "error" → NaN
merged["motion_count"] = merged["motion_count"].fillna(merged["motion_count"].mean())
merged = merged.dropna()
merged.to_csv("merged_sensor_cleaned.csv", index=False)
```


---

## 세션 02. 정규화·인코딩

### 📘 개념

**스케일링**: 특성(Feature) 값의 범위를 조정해서 특정 특성에 편향되지 않게 한다.
| 방법 | 내용 | 언제 |
|---|---|---|
| 표준화(Standardization) | 평균 0, 표준편차 1로 맞춤. 모든 특성이 동일한 분포 | 모델이 특정 특성에 치우치지 않게 |
| 정규화(Normalization) | 값을 0~1 범위로 변환 | 값의 크기 차이가 크고 분포가 일정하지 않을 때 |

**인코딩**: 문자 범주 데이터를 모델이 이해하는 숫자로 바꾸는 과정(대부분의 알고리즘은 숫자만 입력으로 받음).
| 방법 | 내용 | 장점 | 단점 |
|---|---|---|---|
| Label Encoding(정수 인코딩) | 텍스트를 숫자로 | 메모리 효율적, 간단 | 잘못된 경향성(순서·크기)을 학습할 수 있음 |
| One-hot Encoding | 범주를 벡터로 표현 | 순서·크기 관계 제거로 공정한 표현 | 차원 증가, 메모리 사용↑, 희소 행렬 |

**보너스**: 파일 경로 처리 — `os.path.exists`로 존재 여부 확인.

### ✏ 문제 1. 체력 측정 결과 정규화

**지문 요점**
1. `pushup_count`, `run_time_2km`, `situp_count`에 **MinMaxScaler**
2. **원본과 함께** `fitness_scaled.csv` 저장
3. 각 컬럼의 **최소/최대값 출력**

**활용 함수 (PPT '활용 코드 정리')**

- `MinMaxScaler().fit_transform()` — 0~1 정규화  
  ↳ **언제**: "0~1 정규화". 값의 범위가 중요할 때.
- `pd.DataFrame(배열, columns=)` — 배열을 표로 만들기  
  ↳ **언제**: 스케일러 결과(배열)를 다시 표로 만들 때. 열 이름을 꼭 지정.
- `pd.concat([a, b], axis=1)` — 표 이어붙이기(axis=1 옆으로, 0 아래로)  
  ↳ **언제**: 원본 표 옆에 새 열(정규화 결과 등)을 붙일 때(axis=1). 행을 아래로 이으려면 axis=0.
- `Series.min() / max()` — 최솟값 / 최댓값  
  ↳ **언제**: 정규화 결과 범위 확인(0~1인지), 값 범위 점검.

**코드**

> **언제 쓰나**: 지문이 **"0~1 정규화"**이면 MinMaxScaler, **"표준화(평균0·표준편차1)"**이면 StandardScaler. 거리 기반 모델(KMeans, PCA)이나 단위가 다른 열을 비교할 때 사용.

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler
df = pd.read_csv("fitness_test.csv")
cols = ["pushup_count", "run_time_2km", "situp_count"]     # 실제 컬럼명은 df.columns로 확인
scaled = pd.DataFrame(MinMaxScaler().fit_transform(df[cols]), columns=[c + "_scaled" for c in cols])
out = pd.concat([df, scaled], axis=1); out.to_csv("fitness_scaled.csv", index=False)
print(scaled.min(), scaled.max())       # StandardScaler는 평균0·표준편차1
```

### ✏ 문제 2. 보직·지역 인코딩

**지문 요점**
1. `position` → **Label Encoding**, `region` → **One-Hot**
2. `encoded_soldiers.csv` 저장
3. 각 인코딩 컬럼의 **설명 출력**

**활용 함수 (PPT '활용 코드 정리')**

- `LabelEncoder()` — 문자 범주를 정수로  
  ↳ **언제**: 타깃/순서 있는 범주를 정수로. 변환표는 `classes_`로 확인("인코딩 설명 출력").
- `pd.get_dummies(df, columns=)` — 원핫 인코딩  
  ↳ **언제**: 순서 없는 범주(지역 등)를 입력 특성으로 쓸 때. 열이 늘어난다.
- `dict() / list() / zip()` — 딕셔너리·리스트 만들기, 두 목록 짝짓기  
  ↳ **언제**: 인코딩 대응표를 출력하거나 두 목록을 짝지을 때.

**코드**

> **언제 쓰나**: 문자(범주) 열을 모델/계산에 쓸 때. 순서가 의미 있거나 클래스가 2개·타깃(정답) 열이면 **라벨 인코딩**, 순서가 없는 입력 특성(지역, 보직 등)은 **원핫(get_dummies)**.

```python
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv("soldier_info.csv")
le = LabelEncoder(); df["position_enc"] = le.fit_transform(df["position"])
print(dict(zip(le.classes_, le.transform(le.classes_))))   # 인코딩 설명 출력
df = pd.get_dummies(df, columns=["region"], dtype=int)      # 원핫: 순서 없는 범주(지역 등). 라벨 인코딩은 정답열/순서 있는 범주
df.to_csv("encoded_soldiers.csv", index=False)
```

### ✏ 문제 3. 영상 경로 유효성 검사

**지문 요점**
1. `file_path`에 **실제 존재하는 파일만** 필터링
2. `exists`(True/False) 컬럼 추가
3. 있는 것 `valid_videos.csv`, 없는 것 `missing_videos.csv`로 저장

**활용 함수 (PPT '활용 코드 정리')**

- `lambda 입력: 식` — 이름 없는 짧은 함수  
  ↳ **언제**: `apply` 안에서 한 줄짜리 간단한 처리를 할 때.
- `os.path.exists(경로)` — 파일이 있는지 True/False  
  ↳ **언제**: 파일/폴더가 실제로 있는지 확인할 때.

**코드**

> **언제 쓰나**: 표에 파일 경로가 있고 "실제 있는 것만 남겨라"일 때. `apply(os.path.exists)`로 True/False 열을 만든 뒤 필터링.

```python
df = pd.read_csv("video_metadata.csv")
df["exists"] = df["file_path"].apply(lambda p: os.path.exists(p))
df[df["exists"]].to_csv("valid_videos.csv", index=False)
df[~df["exists"]].to_csv("missing_videos.csv", index=False)
```


---

## 세션 03. 시계열 정렬·리샘플링 / JSON

### 📘 개념

**시계열 데이터**: 시간의 흐름에 따라 순서대로 기록된 데이터. 시간 정보(날짜·시각)가 있고 그에 따라 값이 변한다.
- 특징: **시간 종속성**, **추세(Trend)**, **계절성(Seasonality)**, **불규칙성(Irregularity)**
- 리샘플링 주기: 분 `min`, 시간 `H`, 일 `D`, 주 `W`, 월 `M`, 분기 `Q`, 연도 `Y`/`A`
- JSON → 표: `json.load` → `json_normalize` → `rename`

### ✏ 문제 1. 센서 로그 시간대별 통계

**지문 요점**
1. `timestamp`를 datetime으로 바꾸고 **정렬**
2. 감지 횟수를 **1시간 단위 합계**로 리샘플링
3. `hourly_motion.csv` 저장 + **시계열 그래프**

**활용 함수 (PPT '활용 코드 정리')**

- `pd.to_datetime()` — 문자를 날짜 형식으로  
  ↳ **언제**: 날짜가 문자열일 때 반드시 먼저 변환(정렬·리샘플링 전제).
- `sort_values() / set_index()` — 정렬 / 열을 인덱스로(inplace=True면 원본 변경)  
  ↳ **언제**: 시간순 정렬 후 날짜를 인덱스로 둬야 `resample`이 된다.
- `resample('H').sum()` — 시간 단위로 묶어 집계. 주기: min,H,D,W,M,Q,Y  
  ↳ **언제**: "시간/일/주 단위로 합계(sum)·평균(mean)". 지문의 단위에 맞게 주기를 고른다.
- `plt.title/xlabel/ylabel/grid/tight_layout/savefig` — 제목·축·격자·여백·저장  
  ↳ **언제**: 모든 그래프의 마무리. 저장 후 `plt.close()`.

**코드**

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

### ✏ 문제 2. 보급 기록 JSON → CSV

**지문 요점**
1. JSON을 `unit, supply_date, water, ration, medicine` 컬럼의 DataFrame으로
2. `supply_log.csv` 저장
3. 항목별 **총합 출력**

**활용 함수 (PPT '활용 코드 정리')**

- `with open() / json.load()` — JSON 파일 읽기  
  ↳ **언제**: `.json` 파일을 파이썬 객체로 읽을 때.
- `pd.json_normalize()` — 중첩 JSON을 표로  
  ↳ **언제**: 중첩된 JSON(안에 딕셔너리)을 한 줄 표로 펼칠 때.
- `df.rename(columns={})` — 열 이름 바꾸기  
  ↳ **언제**: 열 이름을 지문이 요구한 이름으로 바꿀 때.

**코드**

> **언제 쓰나**: 입력이 `.json`이거나 한 칸 안에 딕셔너리가 중첩(`items`)되어 있을 때. 중첩이면 `json_normalize`, 컬럼명은 `rename`으로 정리.

```python
import json
with open("supply.json", encoding="utf-8") as f: data = json.load(f)
df = pd.json_normalize(data)
df = df.rename(columns={"items.water": "water", "items.ration": "ration", "items.medicine": "medicine"})
df.to_csv("supply_log.csv", index=False)
print(df[["water", "ration", "medicine"]].sum())
```


---

## 세션 04. 기술통계량

### 📘 개념

**기술통계량**: 데이터의 전반적인 특성·분포를 요약하는 수치 지표. 용도: 분포 파악 / 이상치 탐지 / 모델링 전 전처리 참고.
| 지표 | 뜻 |
|---|---|
| 평균(Mean) | 모든 값의 합 ÷ 데이터 수 |
| 중앙값(Median) | 정렬했을 때 가운데 값 |
| 최빈값(Mode) | 가장 자주 나타나는 값 |
| 분산(Variance) | 각 값이 평균에서 떨어진 정도를 제곱해 평균낸 값 |
| 표준편차(Std) | 분산의 제곱근(원래 단위와 같아 해석이 쉬움) |
| 범위(Range) | 최댓값 − 최솟값 |
| 사분위 범위(IQR) | Q3(75%) − Q1(25%), 중간 50% 데이터의 범위 |

### ✏ 문제 1~3. 부대별 통계 / 장비 사용 분포 / 설문 요약

**지문 요점**
1. 전체와 **부대(그룹)별** 평균·중앙값·표준편차
2. 평균·표준편차·최소·최대·중앙값, 최빈값
3. 결과를 csv로 저장(`health_stats.csv` 등)

**활용 함수 (PPT '활용 코드 정리')**

- `df.agg([...])` — 여러 통계를 한 번에  
  ↳ **언제**: 여러 통계(평균·중앙값·표준편차)를 한 번에 구할 때.
- `mode() / var() / quantile()` — 최빈값 / 분산 / 분위수  
  ↳ **언제**: 최빈값(자주 나온 값), 분산, 사분위수(IQR 계산)가 필요할 때.
- `str.strip() / '구분자'.join()` — 문자 앞뒤 공백 제거 / 문자 이어붙이기  
  ↳ **언제**: 문자열 앞뒤 공백 정리, 열 이름 평탄화 등 문자열 가공.
- `Series.to_frame() / df.T` — 시리즈를 표로 / 행·열 뒤집기(전치)  
  ↳ **언제**: 시리즈를 표로 바꾸거나, 행·열을 뒤집어 보기 좋게 만들 때.
- `iloc[] / loc[]` — 번호로 선택 / 이름·조건으로 선택  
  ↳ **언제**: 번호로 고를 땐 `iloc`, 이름/조건으로 고를 땐 `loc`.

**코드**

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


---

## 세션 05. 데이터 시각화

### 📘 개념

- 도구: **matplotlib**, **seaborn**, plotly
- 차트: 막대(bar), 히스토그램, 박스플롯, 산점도, 파이 등
  - 히스토그램 = 분포 / 박스플롯 = 분포와 이상치 / 산점도 = 두 변수 관계
- **상관계수**(피어슨, `corr()`): −1~1. 부호는 방향, 절댓값이 클수록 관계가 강함. **heatmap**으로 한 번에 시각화.

### ✏ 문제 1~3. 분포·이상치 / 산점도·상관 / 상관 heatmap

**지문 요점**
1. 히스토그램+박스플롯 → `plots/` 폴더에 저장
2. `training_pressure`–`command_tension` **산점도**
3. **상관계수 행렬 + heatmap**을 png로 저장

**활용 함수 (PPT '활용 코드 정리')**

- `os.makedirs(폴더, exist_ok=True)` — 폴더 만들기(있어도 오류 안 남)  
  ↳ **언제**: 그래프 저장 폴더가 없을 때 먼저 만들기(`savefig` 오류 방지).
- `plt.subplot() / plt.subplots()` — 한 화면에 그래프 여러 개  
  ↳ **언제**: 한 이미지에 그래프 여러 개를 배치해 저장할 때.
- `plt.hist() / plt.boxplot()` — 히스토그램 / 박스플롯(이상치 확인)  
  ↳ **언제**: 분포 확인은 hist, 이상치 확인은 boxplot.
- `sns.scatterplot() / plt.legend()` — 산점도 / 범례 표시  
  ↳ **언제**: 두 변수의 관계, 그룹별 색 구분은 `hue`와 legend.
- `df.corr() / sns.heatmap(annot=True)` — 상관계수 표 / 열지도  
  ↳ **언제**: 여러 숫자 열의 상관관계를 한 번에 볼 때.

**코드**

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


---

## 세션 06. 데이터 해석

### 📘 개념

- **상관관계로 해석**: 상관계수의 부호와 크기로 "어떤 관계인지" 문장으로 설명.
- **임계치(threshold)로 해석**: 기준값(중앙값 등)을 정해 높은 그룹/낮은 그룹으로 나눠 평균 비교.
- **groupby + mean**: 그룹별 평균. **idxmin/idxmax**: 가장 낮은/높은 항목 이름.
- **pivot_table** 4요소: ① 대상 DataFrame ② `index`(행) ③ `values`(값) ④ `aggfunc`(집계 방법)
- 지표 방향 주의: 수리 횟수처럼 **낮을수록 좋은** 지표가 있다.

### ✏ 문제 1~3. 관계 해석 / 그룹 통계 / 운용 효율

**지문 요점**
1. 두 변수의 **상관계수 + 해석**
2. **임계치**로 높은/낮은 그룹 평균 비교
3. `groupby` 평균, 가장 낮은 항목, `pivot_table`로 구조화

**활용 함수 (PPT '활용 코드 정리')**

- `round(값, 자리)` — 반올림  
  ↳ **언제**: 출력/해석용 숫자 정리. 저장 파일 값은 지문 요구에 맞춘다.
- `임계치(threshold)로 그룹 나누기` — 기준값보다 높음/낮음 비교  
  ↳ **언제**: "높은/낮은 그룹 비교". 기준은 중앙값·평균·지문이 준 값.
- `groupby().mean()` — 그룹별 평균  
  ↳ **언제**: "~별 평균"(부대별, 유형별, 군집별).
- `Series.idxmin() / idxmax()` — 가장 작은/큰 값의 이름(인덱스)  
  ↳ **언제**: "가장 낮은/높은 항목의 이름"을 물을 때.
- `pd.pivot_table(df, index, values, aggfunc)` — 행=그룹, 값=집계로 요약표  
  ↳ **언제**: "표로 요약/구조화"할 때(행=그룹, 값=집계).

**코드**

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


---

## 세션 07. 지도학습 및 평가

### 📘 개념

**머신러닝**: 데이터를 스스로 학습해 특징을 찾고, 새 데이터의 결과를 예측하는 모델.
| 구분 | 설명 | 종류 |
|---|---|---|
| 지도학습 | 정답을 함께 주고 정답을 학습 | **분류**(클래스로 분류), **회귀**(연속값 예측) |
| 비지도학습 | 정답 없이 데이터의 특성을 스스로 학습 | **군집화**, **차원 축소** |

**분류 평가** (혼동행렬 기반, 일반 정의)
| 지표 | 뜻 |
|---|---|
| 혼동행렬 | 예측 클래스 vs 실제 클래스를 행렬로 표시 |
| 정확도 | 전체 중 맞춘 비율 |
| 정밀도 | 양성이라 예측한 것 중 실제 양성 비율 |
| 재현율 | 실제 양성 중 맞춘 비율 |
| F1-score | 정밀도와 재현율의 조화평균 |

**회귀 평가**
| 지표 | 뜻 |
|---|---|
| MAE | 예측값과 실제값의 절대 오차 평균. 작을수록 좋음 |
| MSE | 오차 제곱의 평균. 이상치에 민감 |
| RMSE | MSE의 제곱근. 이상치 민감도를 고려하면서 직관적 |
| R² | 모델이 데이터를 얼마나 설명하는지. 1에 가까울수록 좋음 |

**모델**: 분류 = RandomForestClassifier, GradientBoostingClassifier / 회귀 = LinearRegression. 학습 `fit()`, 예측 `predict()`, 분할 `train_test_split()`(X=특징, y=타깃).

### ✏ 문제 1. 전투 적합도 분류

**지문 요점**
1. `status`를 Label Encoding(적합=1, 부적합=0)
2. **8:2 분할** 후 RandomForestClassifier 학습
3. 예측 결과 csv 저장 + 정확도·혼동행렬·classification_report 출력

**활용 함수 (PPT '활용 코드 정리')**

- `train_test_split()` — 학습/테스트 분리  
  ↳ **언제**: 모델을 만들 때 항상 먼저. 평가는 **테스트셋**으로. 보통 `test_size=0.2, random_state=42`.
- `RandomForestClassifier / fit / predict` — 분류 모델 학습·예측  
  ↳ **언제**: 타깃이 범주. `fit`으로 학습 → `predict`로 예측.
- `accuracy_score / confusion_matrix / classification_report` — 분류 평가  
  ↳ **언제**: 분류 모델 평가. 지문에 적힌 지표를 모두 출력.

**코드**

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

### ✏ 문제 2. 장비 수명 예측(회귀)

**지문 요점**
1. **LinearRegression** 학습
2. 테스트 데이터 예측 + **RMSE**
3. `life_prediction.csv`(`equipment_id, predicted_life`) + 실제 vs 예측 그래프 저장

**활용 함수 (PPT '활용 코드 정리')**

- `LinearRegression` — 회귀 모델  
  ↳ **언제**: 타깃이 숫자이고 지문이 선형회귀를 지정했을 때.
- `mean_squared_error → RMSE` — 회귀 평가(RMSE = MSE의 제곱근)  
  ↳ **언제**: 회귀 평가. RMSE는 작을수록 좋음. 시험 환경에선 `np.sqrt(mean_squared_error)`.

**코드**

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

### ✏ 문제 3. 정비 시급성 다중분류

**지문 요점**
1. `priority_level`(A/B/C)을 Label Encoding
2. GradientBoosting 또는 RandomForest 다중 분류
3. classification_report·confusion_matrix + `priority_prediction.csv`

**활용 함수 (PPT '활용 코드 정리')**

- `GradientBoostingClassifier` — 다중분류 모델  
  ↳ **언제**: 3개 이상 클래스 분류. RandomForest와 같은 방식으로 `fit/predict`.

**코드**

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


---

## 세션 08. 비지도학습

### 📘 개념

| 방법 | 설명 |
|---|---|
| 군집화 | 레이블 없는 데이터를 유사성에 따라 그룹(클러스터)으로 나눔. 데이터의 내재된 구조 파악, EDA에 유용 (`KMeans(n_clusters)`) |
| 차원 축소 | 고차원 데이터를 저차원으로 변환해 간소화, 중요한 패턴 유지 (`PCA`, `pca.components_`) |

**실루엣 계수**(군집이 잘 나뉘었는지): a(i) = 같은 군집 내 다른 점들과의 평균 거리, b(i) = 가장 가까운 다른 군집 점들과의 평균 거리. 일반식 s = (b − a) / max(a, b), −1~1이고 **클수록 좋음**.

### ✏ 문제 1~3. 군집화 / PCA 2차원 / 근무 유형 군집

**지문 요점**
1. `KMeans(n_clusters=3)`, 결과 `cluster` 컬럼 저장
2. **StandardScaler → PCA 2차원** 후 산점도
3. `groupby('cluster').mean()`으로 군집 특성 해석

**활용 함수 (PPT '활용 코드 정리')**

- `KMeans(n_clusters=3)` — 군집화. 결과는 .labels_  
  ↳ **언제**: 정답 없이 N개 그룹으로 묶을 때. 군집 수는 지문이 정한다. 먼저 표준화.
- `PCA(n_components=2) / pca.components_` — 2차원 축소 / 축 구성 확인  
  ↳ **언제**: 열이 많을 때 2차원으로 줄여 시각화. `components_`로 각 축에 어떤 열이 크게 기여하는지 해석.
- `silhouette_score` — 군집 분리 정도(−1~1, 클수록 좋음)  
  ↳ **언제**: 군집이 잘 나뉘었는지 점수로 확인(1에 가까울수록 좋음).

**코드**

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


---

## 세션 09. 이미지 처리 (OpenCV)

### 📘 개념

- **OpenCV**: 컴퓨터 비전·머신러닝 오픈소스 라이브러리. 실시간 이미지 처리 중심(이미지·영상 처리, 객체 탐지 등).
- 학습 포인트: ① 이미지 읽고 처리 ② 윤곽선·도형 검출 ③ 객체 좌표 추출·데이터화
- 흐름: `imread`(BGR) → `cvtColor`(흑백) → `resize` → `GaussianBlur` → `Canny` → `findContours` → `approxPolyDP`/`arcLength`/`isContourConvex` → `boundingRect`
- **YOLO**: 사전학습 모델로 객체 탐지(클래스명, 좌표 x1·y1·x2·y2, 신뢰도).

### ✏ 문제 1. 이미지 밝기

**지문 요점**
1. 모든 이미지를 **256×256 리사이즈 → 흑백 → 평균 밝기**
2. `brightness_result.csv` 저장, 가장 밝은 파일명 출력

**활용 함수 (PPT '활용 코드 정리')**

- `cv2.imread(경로)` — 이미지 읽기(색 순서 BGR)
- `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` — 흑백 변환
- `cv2.resize(img, (256, 256))` — 크기 변경(가로, 세로)

**코드**

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

### ✏ 문제 2. 설계도 사각형 검출

**지문 요점**
1. `findContours`로 윤곽 검출
2. `approxPolyDP`로 **사각형만** 필터링
3. 이미지별 (x,y,width,height)와 사각형 수를 `rectangles.csv`에 저장

**활용 함수 (PPT '활용 코드 정리')**

- `cv2.GaussianBlur(img, (5,5), 0)` — 흐리게(잡음 제거)
- `cv2.Canny(img, 50, 150)` — 윤곽선(엣지) 검출
- `cv2.findContours(...)` — 윤곽 찾기
- `cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)` — 윤곽을 꼭짓점 N개 도형으로 단순화
- `cv2.isContourConvex(ap)` — 볼록 도형인지
- `cv2.boundingRect(ap)` — 외접 사각형 (x, y, w, h)

**코드**

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

### ✏ 문제 3. 객체 탐지(YOLO)와 좌표 저장

**지문 요점**
1. 사전학습 **YOLOv5**로 사람·차량 탐지
2. 클래스명과 (x1,y1,x2,y2) 추출
3. `detections.csv`(`filename, class, x1, y1, x2, y2`), 사람/차량 수 출력

**활용 함수 (PPT '활용 코드 정리')**

- `PIL.Image.open(경로)` — 이미지 열기
- `torch.hub.load('ultralytics/yolov5','yolov5s', pretrained=True)` — YOLOv5 모델 불러오기
- `results.pandas().xyxy[0]` — 탐지 결과 표(`xmin ymin xmax ymax confidence class name`)

**코드**

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

> **언제 쓰나**: `torch.hub.load`가 안 될 때. `pip install ultralytics` 후 `YOLO('yolov8n.pt')`. 가장 작은 모델(n)이 CPU에서 빠름.

```python
# pip install ultralytics
from ultralytics import YOLO
model = YOLO("yolov8n.pt")            # 가중치 다운로드 필요
r = model.predict("img.png", device="cpu", verbose=False)[0]
for (x1, y1, x2, y2), c in zip(r.boxes.xyxy.tolist(), r.boxes.cls.tolist()):
    print(r.names[int(c)], x1, y1, x2, y2)            # COCO: person=0, car=2, bus=5, truck=7
```


---

## 세션 10. 이미지 분류·OCR·영상

### 📘 개념

- 탐지 결과를 **통계화**(클래스별 빈도) → `Counter`, 상위 N개 막대그래프
- **OCR**: 이미지 속 글자 인식(`easyocr.Reader`, `readtext`), 정규식 `re`로 한글·영문·숫자만 추출
- **영상**: `cv2.VideoCapture` → `isOpened()` → `read()`로 프레임 추출(예: 30FPS면 30프레임마다 1초 간격)
- 이미지에서 추출한 정보를 표로 만들어 csv로 저장

### ✏ 문제 1. 객체 빈도 통계

**지문 요점**
1. 각 이미지에 YOLO 탐지
2. 클래스별 **전체 빈도**를 `object_count.csv`에
3. **상위 3개** 막대그래프 `top3_objects.png`

**활용 함수 (PPT '활용 코드 정리')**

- `[f for f in os.listdir(d) if f.lower().endswith(('.jpg','.png','.jpeg'))]` — 폴더에서 이미지 파일만 모으기
- `collections.Counter(리스트)` / `.most_common(3)` — 빈도 세기 / 상위 3개

**코드**

> **언제 쓰나**: "탐지된 객체의 빈도/상위 N개"일 때 `Counter`(`most_common(N)`) 후 막대그래프.

```python
from collections import Counter
cnt = Counter(det["class"])                         # 위에서 만든 detections 사용
pd.DataFrame(cnt.items(), columns=["class", "count"]).sort_values("count", ascending=False).to_csv("object_count.csv", index=False)
top3 = cnt.most_common(3)
plt.bar([k for k, _ in top3], [v for _, v in top3]); plt.title("Top3 objects"); plt.savefig("top3_objects.png"); plt.close()
```

### ✏ 문제 2. 이미지 속 글자(OCR)

**지문 요점**
1. `easyocr`로 텍스트 추출
2. **정규식**으로 한글·영문·숫자만 남김
3. `supply_info.csv` 저장

**활용 함수 (PPT '활용 코드 정리')**

- `easyocr.Reader(['ko','en'])` / `readtext(경로)` — 글자 인식 모델 / 인식 실행 → (좌표, 글자, 신뢰도)
- `re.match(r'^[가-힣A-Za-z0-9]+$', text)` — 정규식으로 한글·영문·숫자만 통과

**코드**

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

### ✏ 문제 3. 드론 영상 프레임 탐지

**지문 요점**
1. **1초 간격**으로 프레임 추출(30FPS → 30프레임마다)
2. 각 프레임 YOLO 탐지
3. `drone_detection.csv`(`frame_number, class, x1, y1, x2, y2`) + 프레임별 개수 시계열 그래프

**활용 함수 (PPT '활용 코드 정리')**

- `cv2.VideoCapture(경로)` / `isOpened()` / `read()` — 영상 열기 / 열렸는지 / 프레임 한 장 읽기(`ok, frame`)
- `cap.get(cv2.CAP_PROP_FPS)` — 초당 프레임 수

**코드**

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
