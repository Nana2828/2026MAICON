# 함수 색인 (PPT '활용 코드 정리' 기반)

> 수업 PPT의 각 세션 `활용 코드 정리` 슬라이드에 나온 함수를 세션별로 **뜻 + 한 줄 예시**로 정리했습니다. 시험 중 "이 함수 뭐였지?" 할 때 `Ctrl+F`로 찾으세요.
> 예시는 `df = pd.read_csv('maintenance_log.csv')`(세션 01 실습 데이터)를 기준으로 실행 확인했습니다. 열 이름은 지문에 맞게 바꿔 쓰세요.

공통: `import pandas as pd, numpy as np`


## 세션 01 결측·이상치

### `pd.read_csv() / df.to_csv()`
파일 읽기 / 저장
```python
df = pd.read_csv('maintenance_log.csv')
df.to_csv('out.csv', index=False)
```

### `df.head() / df.describe()`
앞 5줄 / 숫자 열 요약통계
```python
df.head(); df.describe()
```

### `df.info() / df.shape`
열 타입·결측 확인 / (행,열) 크기
```python
df.info(); df.shape
```

### `df['컬럼']`
열 하나 고르기(Series)
```python
df['repair_count']
```

### `fillna(값)`
빈칸 채우기
```python
df['repair_count'].fillna(0)
```

### `Series.mean() / median() / std()`
평균 / 중앙값 / 표준편차
```python
df['repair_count'].mean(), df['repair_count'].median()
```

### `scipy.stats.zscore`
표준점수(Z). 절댓값 3 초과=이상치
```python
from scipy.stats import zscore
z = zscore(df['repair_duration'].dropna())
```

### `df[조건식]`
조건에 맞는 행만 선택
```python
df[df['repair_count'] > 3]
```

### `apply()`
각 열/값에 함수 적용
```python
df[['repair_count','repair_duration']].apply(lambda s: s - s.mean())
```

### `drop()`
행/열 삭제
```python
df.drop(columns=['date'])  # 행 삭제: df.drop(index=[0,1])
```

### `dropna()`
빈칸이 있는 행 삭제
```python
df.dropna(); df.dropna(subset=['repair_count'])
```

### `pd.merge(a, b, on=, suffixes=)`
두 표를 기준 열로 합치기. 겹치는 열 이름 구분
```python
a = df[['equipment_id','repair_count']]; b = df[['equipment_id','repair_duration']]
pd.merge(a, b, on='equipment_id', suffixes=('_a','_b'))
```


## 세션 02 정규화·인코딩

### `MinMaxScaler().fit_transform()`
0~1 정규화
```python
from sklearn.preprocessing import MinMaxScaler
MinMaxScaler().fit_transform(df[['repair_count']].fillna(0))
```

### `StandardScaler().fit_transform()`
평균0·표준편차1 표준화
```python
from sklearn.preprocessing import StandardScaler
StandardScaler().fit_transform(df[['repair_count']].fillna(0))
```

### `pd.DataFrame(배열, columns=)`
배열을 표로 만들기
```python
pd.DataFrame([[1,2],[3,4]], columns=['a','b'])
```

### `pd.concat([a, b], axis=1)`
표 이어붙이기(axis=1 옆으로, 0 아래로)
```python
pd.concat([df[['equipment_id']], df[['repair_count']]], axis=1)
```

### `Series.min() / max()`
최솟값 / 최댓값
```python
df['repair_count'].min(), df['repair_count'].max()
```

### `LabelEncoder()`
문자 범주를 정수로
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder(); le.fit_transform(df['equipment_id'])[:5]; le.classes_[:3]
```

### `pd.get_dummies(df, columns=)`
원핫 인코딩
```python
pd.get_dummies(df[['equipment_id']].head(), columns=['equipment_id'], dtype=int)
```

### `dict() / list() / zip()`
딕셔너리·리스트 만들기, 두 목록 짝짓기
```python
dict(zip(le.classes_[:3], range(3)))
```

### `lambda 입력: 식`
이름 없는 짧은 함수
```python
df['equipment_id'].apply(lambda x: x.lower()).head()
```

### `os.path.exists(경로)`
파일이 있는지 True/False
```python
import os
os.path.exists('maintenance_log.csv')
```


## 세션 03 시계열·JSON

### `pd.to_datetime()`
문자를 날짜 형식으로
```python
df['date'] = pd.to_datetime(df['date'])
```

### `sort_values() / set_index()`
정렬 / 열을 인덱스로(inplace=True면 원본 변경)
```python
d2 = df.sort_values('date').set_index('date')
```

### `resample('H').sum()`
시간 단위로 묶어 집계. 주기: min,H,D,W,M,Q,Y
```python
d2['repair_count'].resample('W').sum().head()
```

### `with open() / json.load()`
JSON 파일 읽기
```python
import json, io
obj = json.load(io.StringIO('[{"unit":"1","items":{"water":3}}]'))
```

### `pd.json_normalize()`
중첩 JSON을 표로
```python
pd.json_normalize(obj)
```

### `df.rename(columns={})`
열 이름 바꾸기
```python
pd.json_normalize(obj).rename(columns={'items.water':'water'})
```


## 세션 04 기술통계

### `df.agg([...])`
여러 통계를 한 번에
```python
df[['repair_count']].agg(['mean','median','std'])
```

### `mode() / var() / quantile()`
최빈값 / 분산 / 분위수
```python
df['repair_count'].mode(); df['repair_count'].var(); df['repair_count'].quantile([.25,.75])
```

### `str.strip() / '구분자'.join()`
문자 앞뒤 공백 제거 / 문자 이어붙이기
```python
'  a '.strip(); '_'.join(['a','b'])
```

### `Series.to_frame() / df.T`
시리즈를 표로 / 행·열 뒤집기(전치)
```python
s = df['repair_count'].describe().to_frame(); s.T
```

### `iloc[] / loc[]`
번호로 선택 / 이름·조건으로 선택
```python
df.iloc[0:3, 0:2]; df.loc[0, 'equipment_id']
```


## 세션 05 시각화

### `os.makedirs(폴더, exist_ok=True)`
폴더 만들기(있어도 오류 안 남)
```python
os.makedirs('plots', exist_ok=True)
```

### `plt.subplot() / plt.subplots()`
한 화면에 그래프 여러 개
```python
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2)
```

### `plt.hist() / plt.boxplot()`
히스토그램 / 박스플롯(이상치 확인)
```python
plt.hist(df['repair_count'].dropna()); plt.boxplot(df['repair_count'].dropna())
```

### `sns.scatterplot() / plt.legend()`
산점도 / 범례 표시
```python
import seaborn as sns
sns.scatterplot(data=df, x='repair_count', y='repair_duration'); plt.legend()
```

### `df.corr() / sns.heatmap(annot=True)`
상관계수 표 / 열지도
```python
sns.heatmap(df.select_dtypes('number').corr(), annot=True)
```

### `plt.title/xlabel/ylabel/grid/tight_layout/savefig`
제목·축·격자·여백·저장
```python
plt.title('t'); plt.xlabel('x'); plt.grid(True); plt.tight_layout(); plt.savefig('a.png'); plt.close()
```


## 세션 06 해석

### `round(값, 자리)`
반올림
```python
round(df['repair_count'].mean(), 2)
```

### `임계치(threshold)로 그룹 나누기`
기준값보다 높음/낮음 비교
```python
th = df['repair_count'].median()
hi = df[df['repair_count'] > th]['repair_duration'].mean()
```

### `groupby().mean()`
그룹별 평균
```python
df.groupby('equipment_id')[['repair_count']].mean().head()
```

### `Series.idxmin() / idxmax()`
가장 작은/큰 값의 이름(인덱스)
```python
df[['repair_count','repair_duration']].mean().idxmin()
```

### `pd.pivot_table(df, index, values, aggfunc)`
행=그룹, 값=집계로 요약표
```python
pd.pivot_table(df, index='equipment_id', values='repair_count', aggfunc='mean').head()
```


## 세션 07 지도학습

### `train_test_split()`
학습/테스트 분리
```python
from sklearn.model_selection import train_test_split
X = df[['repair_count','repair_duration']].fillna(0); y = df['last_check_day'].fillna(0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
```

### `RandomForestClassifier / fit / predict`
분류 모델 학습·예측
```python
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=42).fit(Xtr, (ytr>15)); pred = clf.predict(Xte)
```

### `accuracy_score / confusion_matrix / classification_report`
분류 평가
```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy_score(yte>15, pred); confusion_matrix(yte>15, pred)
```

### `LinearRegression`
회귀 모델
```python
from sklearn.linear_model import LinearRegression
reg = LinearRegression().fit(Xtr, ytr); p = reg.predict(Xte)
```

### `mean_squared_error → RMSE`
회귀 평가(RMSE = MSE의 제곱근)
```python
import numpy as np
from sklearn.metrics import mean_squared_error
np.sqrt(mean_squared_error(yte, p))
```

### `GradientBoostingClassifier`
다중분류 모델
```python
from sklearn.ensemble import GradientBoostingClassifier
GradientBoostingClassifier(random_state=42).fit(Xtr, (ytr>15))
```


## 세션 08 비지도학습

### `KMeans(n_clusters=3)`
군집화. 결과는 .labels_
```python
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X); km.labels_[:5]
```

### `PCA(n_components=2) / pca.components_`
2차원 축소 / 축 구성 확인
```python
from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(X); pca.components_
```

### `silhouette_score`
군집 분리 정도(−1~1, 클수록 좋음)
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
