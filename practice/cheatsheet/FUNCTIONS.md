# 함수 색인 (PPT '활용 코드 정리' 기반)

> 수업 PPT의 각 세션 `활용 코드 정리` 슬라이드에 나온 함수를 세션별로 **뜻 + 한 줄 예시**로 정리했습니다. 시험 중 "이 함수 뭐였지?" 할 때 `Ctrl+F`로 찾으세요.
> 예시는 `df = pd.read_csv('maintenance_log.csv')`(세션 01 실습 데이터)를 기준으로 실행 확인했습니다. 열 이름은 지문에 맞게 바꿔 쓰세요.

공통: `import pandas as pd, numpy as np`


## 세션 01 결측·이상치

### `pd.read_csv() / df.to_csv()`
파일 읽기 / 저장
> **언제**: 파일을 열 때 / 결과를 낼 때. 저장은 항상 `index=False`.

```python
df = pd.read_csv('maintenance_log.csv')
df.to_csv('out.csv', index=False)
```

### `df.head() / df.describe()`
앞 5줄 / 숫자 열 요약통계
> **언제**: 데이터를 처음 볼 때(열 이름, 값 범위, 이상한 값 확인).

```python
df.head(); df.describe()
```

### `df.info() / df.shape`
열 타입·결측 확인 / (행,열) 크기
> **언제**: 열 타입과 빈칸 수, 행 개수를 한눈에 볼 때.

```python
df.info(); df.shape
```

### `df['컬럼']`
열 하나 고르기(Series)
> **언제**: 열 하나만 계산·수정할 때. 여러 열은 `df[['a','b']]`(대괄호 2개).

```python
df['repair_count']
```

### `fillna(값)`
빈칸 채우기
> **언제**: "빈칸을 ~로 채워라". 값은 평균/중앙값/0/최빈값 중 지문이 정한 것.

```python
df['repair_count'].fillna(0)
```

### `Series.mean() / median() / std()`
평균 / 중앙값 / 표준편차
> **언제**: 평균은 보통 값, 중앙값은 극단값이 있을 때, 표준편차는 흩어진 정도.

```python
df['repair_count'].mean(), df['repair_count'].median()
```

### `scipy.stats.zscore`
표준점수(Z). 절댓값 3 초과=이상치. **scipy가 안 될 때는 pandas로: `(s - s.mean()) / s.std(ddof=0)`** (같은 값)
> **언제**: "Z-score로 이상치". scipy가 안 되면 `(x-x.mean())/x.std(ddof=0)`.

```python
from scipy.stats import zscore
z = zscore(df['repair_duration'].dropna())
```

### `df[조건식]`
조건에 맞는 행만 선택
> **언제**: "~인 행만 남겨라/골라라". 조건 여러 개는 `(a) & (b)`, `|`로 묶고 각각 괄호.

```python
df[df['repair_count'] > 3]
```

### `apply()`
각 열/값에 함수 적용
> **언제**: 각 열/값에 함수를 한꺼번에 적용할 때(예: 열마다 zscore).

```python
df[['repair_count','repair_duration']].apply(lambda s: s - s.mean())
```

### `drop()`
행/열 삭제
> **언제**: 열을 지울 때 `columns=[...]`, 행을 지울 때 `index=[...]`. 임시 컬럼 정리에 사용.

```python
df.drop(columns=['date'])  # 행 삭제: df.drop(index=[0,1])
```

### `dropna()`
빈칸이 있는 행 삭제
> **언제**: "빈칸 있는 행은 제거". 특정 열만 보려면 `subset=[...]`.

```python
df.dropna(); df.dropna(subset=['repair_count'])
```

### `pd.merge(a, b, on=, suffixes=)`
두 표를 기준 열로 합치기. 겹치는 열 이름 구분
> **언제**: 파일/표가 두 개 이상이고 "합쳐라". 기준 열이 같아야 하고 겹치는 열은 `suffixes`로 구분.

```python
a = df[['equipment_id','repair_count']]; b = df[['equipment_id','repair_duration']]
pd.merge(a, b, on='equipment_id', suffixes=('_a','_b'))
```


## 세션 02 정규화·인코딩

### `MinMaxScaler().fit_transform()`
0~1 정규화
> **언제**: "0~1 정규화". 값의 범위가 중요할 때.

```python
from sklearn.preprocessing import MinMaxScaler
MinMaxScaler().fit_transform(df[['repair_count']].fillna(0))
```

### `StandardScaler().fit_transform()`
평균0·표준편차1 표준화
> **언제**: "표준화". 모델·PCA·KMeans 전 열 크기를 맞출 때.

```python
from sklearn.preprocessing import StandardScaler
StandardScaler().fit_transform(df[['repair_count']].fillna(0))
```

### `pd.DataFrame(배열, columns=)`
배열을 표로 만들기
> **언제**: 스케일러 결과(배열)를 다시 표로 만들 때. 열 이름을 꼭 지정.

```python
pd.DataFrame([[1,2],[3,4]], columns=['a','b'])
```

### `pd.concat([a, b], axis=1)`
표 이어붙이기(axis=1 옆으로, 0 아래로)
> **언제**: 원본 표 옆에 새 열(정규화 결과 등)을 붙일 때(axis=1). 행을 아래로 이으려면 axis=0.

```python
pd.concat([df[['equipment_id']], df[['repair_count']]], axis=1)
```

### `Series.min() / max()`
최솟값 / 최댓값
> **언제**: 정규화 결과 범위 확인(0~1인지), 값 범위 점검.

```python
df['repair_count'].min(), df['repair_count'].max()
```

### `LabelEncoder()`
문자 범주를 정수로
> **언제**: 타깃/순서 있는 범주를 정수로. 변환표는 `classes_`로 확인("인코딩 설명 출력").

```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder(); le.fit_transform(df['equipment_id'])[:5]; le.classes_[:3]
```

### `pd.get_dummies(df, columns=)`
원핫 인코딩
> **언제**: 순서 없는 범주(지역 등)를 입력 특성으로 쓸 때. 열이 늘어난다.

```python
pd.get_dummies(df[['equipment_id']].head(), columns=['equipment_id'], dtype=int)
```

### `dict() / list() / zip()`
딕셔너리·리스트 만들기, 두 목록 짝짓기
> **언제**: 인코딩 대응표를 출력하거나 두 목록을 짝지을 때.

```python
dict(zip(le.classes_[:3], range(3)))
```

### `lambda 입력: 식`
이름 없는 짧은 함수
> **언제**: `apply` 안에서 한 줄짜리 간단한 처리를 할 때.

```python
df['equipment_id'].apply(lambda x: x.lower()).head()
```

### `os.path.exists(경로)`
파일이 있는지 True/False
> **언제**: 파일/폴더가 실제로 있는지 확인할 때.

```python
import os
os.path.exists('maintenance_log.csv')
```


## 세션 03 시계열·JSON

### `pd.to_datetime()`
문자를 날짜 형식으로
> **언제**: 날짜가 문자열일 때 반드시 먼저 변환(정렬·리샘플링 전제).

```python
df['date'] = pd.to_datetime(df['date'])
```

### `sort_values() / set_index()`
정렬 / 열을 인덱스로(inplace=True면 원본 변경)
> **언제**: 시간순 정렬 후 날짜를 인덱스로 둬야 `resample`이 된다.

```python
d2 = df.sort_values('date').set_index('date')
```

### `resample('H').sum()`
시간 단위로 묶어 집계. 주기: min,H,D,W,M,Q,Y
> **언제**: "시간/일/주 단위로 합계(sum)·평균(mean)". 지문의 단위에 맞게 주기를 고른다.

```python
d2['repair_count'].resample('W').sum().head()
```

### `with open() / json.load()`
JSON 파일 읽기
> **언제**: `.json` 파일을 파이썬 객체로 읽을 때.

```python
import json, io
obj = json.load(io.StringIO('[{"unit":"1","items":{"water":3}}]'))
```

### `pd.json_normalize()`
중첩 JSON을 표로
> **언제**: 중첩된 JSON(안에 딕셔너리)을 한 줄 표로 펼칠 때.

```python
pd.json_normalize(obj)
```

### `df.rename(columns={})`
열 이름 바꾸기
> **언제**: 열 이름을 지문이 요구한 이름으로 바꿀 때.

```python
pd.json_normalize(obj).rename(columns={'items.water':'water'})
```


## 세션 04 기술통계

### `df.agg([...])`
여러 통계를 한 번에
> **언제**: 여러 통계(평균·중앙값·표준편차)를 한 번에 구할 때.

```python
df[['repair_count']].agg(['mean','median','std'])
```

### `mode() / var() / quantile()`
최빈값 / 분산 / 분위수
> **언제**: 최빈값(자주 나온 값), 분산, 사분위수(IQR 계산)가 필요할 때.

```python
df['repair_count'].mode(); df['repair_count'].var(); df['repair_count'].quantile([.25,.75])
```

### `str.strip() / '구분자'.join()`
문자 앞뒤 공백 제거 / 문자 이어붙이기
> **언제**: 문자열 앞뒤 공백 정리, 열 이름 평탄화 등 문자열 가공.

```python
'  a '.strip(); '_'.join(['a','b'])
```

### `Series.to_frame() / df.T`
시리즈를 표로 / 행·열 뒤집기(전치)
> **언제**: 시리즈를 표로 바꾸거나, 행·열을 뒤집어 보기 좋게 만들 때.

```python
s = df['repair_count'].describe().to_frame(); s.T
```

### `iloc[] / loc[]`
번호로 선택 / 이름·조건으로 선택
> **언제**: 번호로 고를 땐 `iloc`, 이름/조건으로 고를 땐 `loc`.

```python
df.iloc[0:3, 0:2]; df.loc[0, 'equipment_id']
```


## 세션 05 시각화

### `os.makedirs(폴더, exist_ok=True)`
폴더 만들기(있어도 오류 안 남)
> **언제**: 그래프 저장 폴더가 없을 때 먼저 만들기(`savefig` 오류 방지).

```python
os.makedirs('plots', exist_ok=True)
```

### `plt.subplot() / plt.subplots()`
한 화면에 그래프 여러 개
> **언제**: 한 이미지에 그래프 여러 개를 배치해 저장할 때.

```python
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2)
```

### `plt.hist() / plt.boxplot()`
히스토그램 / 박스플롯(이상치 확인)
> **언제**: 분포 확인은 hist, 이상치 확인은 boxplot.

```python
plt.hist(df['repair_count'].dropna()); plt.boxplot(df['repair_count'].dropna())
```

### `sns.scatterplot() / plt.legend()`
산점도 / 범례 표시
> **언제**: 두 변수의 관계, 그룹별 색 구분은 `hue`와 legend.

```python
import seaborn as sns
sns.scatterplot(data=df, x='repair_count', y='repair_duration'); plt.legend()
```

### `df.corr() / sns.heatmap(annot=True)`
상관계수 표 / 열지도
> **언제**: 여러 숫자 열의 상관관계를 한 번에 볼 때.

```python
sns.heatmap(df.select_dtypes('number').corr(), annot=True)
```

### `plt.title/xlabel/ylabel/grid/tight_layout/savefig`
제목·축·격자·여백·저장
> **언제**: 모든 그래프의 마무리. 저장 후 `plt.close()`.

```python
plt.title('t'); plt.xlabel('x'); plt.grid(True); plt.tight_layout(); plt.savefig('a.png'); plt.close()
```


## 세션 06 해석

### `round(값, 자리)`
반올림
> **언제**: 출력/해석용 숫자 정리. 저장 파일 값은 지문 요구에 맞춘다.

```python
round(df['repair_count'].mean(), 2)
```

### `임계치(threshold)로 그룹 나누기`
기준값보다 높음/낮음 비교
> **언제**: "높은/낮은 그룹 비교". 기준은 중앙값·평균·지문이 준 값.

```python
th = df['repair_count'].median()
hi = df[df['repair_count'] > th]['repair_duration'].mean()
```

### `groupby().mean()`
그룹별 평균
> **언제**: "~별 평균"(부대별, 유형별, 군집별).

```python
df.groupby('equipment_id')[['repair_count']].mean().head()
```

### `Series.idxmin() / idxmax()`
가장 작은/큰 값의 이름(인덱스)
> **언제**: "가장 낮은/높은 항목의 이름"을 물을 때.

```python
df[['repair_count','repair_duration']].mean().idxmin()
```

### `pd.pivot_table(df, index, values, aggfunc)`
행=그룹, 값=집계로 요약표
> **언제**: "표로 요약/구조화"할 때(행=그룹, 값=집계).

```python
pd.pivot_table(df, index='equipment_id', values='repair_count', aggfunc='mean').head()
```


## 세션 07 지도학습

### `train_test_split()`
학습/테스트 분리
> **언제**: 모델을 만들 때 항상 먼저. 평가는 **테스트셋**으로. 보통 `test_size=0.2, random_state=42`.

```python
from sklearn.model_selection import train_test_split
X = df[['repair_count','repair_duration']].fillna(0); y = df['last_check_day'].fillna(0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
```

### `RandomForestClassifier / fit / predict`
분류 모델 학습·예측
> **언제**: 타깃이 범주. `fit`으로 학습 → `predict`로 예측.

```python
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=42).fit(Xtr, (ytr>15)); pred = clf.predict(Xte)
```

### `accuracy_score / confusion_matrix / classification_report`
분류 평가
> **언제**: 분류 모델 평가. 지문에 적힌 지표를 모두 출력.

```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy_score(yte>15, pred); confusion_matrix(yte>15, pred)
```

### `LinearRegression`
회귀 모델
> **언제**: 타깃이 숫자이고 지문이 선형회귀를 지정했을 때.

```python
from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(Xtr, ytr); p = reg.predict(Xte)
```

### `mean_squared_error → RMSE`
회귀 평가(RMSE = MSE의 제곱근)
> **언제**: 회귀 평가. RMSE는 작을수록 좋음. 시험 환경에선 `np.sqrt(mean_squared_error)`.

```python
import numpy as np
from sklearn.metrics import mean_squared_error
np.sqrt(mean_squared_error(yte, p))
```

### `GradientBoostingClassifier`
다중분류 모델
> **언제**: 3개 이상 클래스 분류. RandomForest와 같은 방식으로 `fit/predict`.

```python
from sklearn.ensemble import GradientBoostingClassifier
GradientBoostingClassifier(random_state=42).fit(Xtr, (ytr>15))
```


## 세션 08 비지도학습

### `KMeans(n_clusters=3)`
군집화. 결과는 .labels_
> **언제**: 정답 없이 N개 그룹으로 묶을 때. 군집 수는 지문이 정한다. 먼저 표준화.

```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X); km.labels_[:5]
```

### `PCA(n_components=2) / pca.components_`
2차원 축소 / 축 구성 확인
> **언제**: 열이 많을 때 2차원으로 줄여 시각화. `components_`로 각 축에 어떤 열이 크게 기여하는지 해석.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(X); pca.components_
```

### `silhouette_score`
군집 분리 정도(−1~1, 클수록 좋음)
> **언제**: 군집이 잘 나뉘었는지 점수로 확인(1에 가까울수록 좋음).

```python
from sklearn.metrics import silhouette_score
silhouette_score(X, km.labels_)
```


## 세션 09 이미지 처리 (OpenCV) — PPT 목록
| 함수 | 뜻 |
|---|---|
| `cv2.imread(경로)` | 이미지 읽기(색 순서 BGR) |
| `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` | 흑백 변환 |
| `cv2.resize(img, (256, 256))` | 크기 변경(가로, 세로) |
| `cv2.GaussianBlur(img, (5,5), 0)` | 흐리게(잡음 제거) |
| `cv2.Canny(img, 50, 150)` | 윤곽선(엣지) 검출 |
| `cv2.findContours(...)` | 윤곽 찾기 |
| `cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)` | 윤곽을 꼭짓점 몇 개짜리 도형으로 단순화 |
| `cv2.isContourConvex(ap)` | 볼록 도형인지 |
| `cv2.boundingRect(ap)` | 외접 사각형 (x, y, w, h) |
| `PIL.Image.open(경로)` | 이미지 열기 |
| `torch.hub.load('ultralytics/yolov5','yolov5s', pretrained=True)` | YOLOv5 모델 불러오기 |
| `results.pandas().xyxy[0]` | 탐지 결과 표(`xmin ymin xmax ymax confidence class name`) |

## 세션 10 이미지 분류·OCR·영상 — PPT 목록
| 함수 | 뜻 |
|---|---|
| `[f for f in os.listdir(d) if f.lower().endswith(('.jpg','.png','.jpeg'))]` | 폴더에서 이미지 파일만 모으기 |
| `collections.Counter(리스트)` / `.most_common(3)` | 빈도 세기 / 상위 3개 |
| `easyocr.Reader(['ko','en'])` / `readtext(경로)` | 글자 인식 모델 / 인식 실행 → (좌표, 글자, 신뢰도) |
| `re.match(r'^[가-힣A-Za-z0-9]+$', text)` | 정규식으로 한글·영문·숫자만 통과 |
| `cv2.VideoCapture(경로)` / `isOpened()` / `read()` | 영상 열기 / 열렸는지 / 프레임 한 장 읽기(`ok, frame`) |
| `cap.get(cv2.CAP_PROP_FPS)` | 초당 프레임 수 |

(세션 09, 10의 전체 흐름 코드는 `CHEATSHEET.md` 참고)
