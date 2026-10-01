# 공식 교육 세션 01~10 요약

출처: 2026 국방 AI 경진대회 예선 대비 교육(DST) 수업자료. 각 세션은 "문제 3개 → 활용 코드 정리 → 정리" 구조이며, 모든 문제가 **csv/이미지 입력 → 처리 → 결과 csv/png 저장** 패턴입니다.
종합문제(세션 11, 12)는 `../mock_exam/` 참고.

## 한눈에 보기

| 세션 | 주제 | 핵심 도구 | 대표 출력물 |
|---|---|---|---|
| 01 | 결측치·이상치 | `fillna`, `zscore`, `merge`, `dropna` | `*_cleaned.csv` |
| 02 | 정규화·인코딩 | `MinMaxScaler`, `LabelEncoder`, `get_dummies`, `os.path.exists` | `fitness_scaled.csv` 등 |
| 03 | 시계열 정렬·리샘플링, JSON | `to_datetime`, `resample`, `json_normalize` | `hourly_motion.csv` |
| 04 | 기술통계량 | `agg`, `groupby`, `mode`, `.T` | `*_stats.csv` |
| 05 | 시각화 | `hist`, `boxplot`, `scatterplot`, `corr`+`heatmap` | `*.png` |
| 06 | 데이터 해석 | `corr`, 임계치 비교, `groupby`, `idxmin`, `pivot_table` | `*_avg.csv` |
| 07 | 지도학습·평가 | `RandomForest*`, `LinearRegression`, `GradientBoosting*`, 평가지표 | `*_result.csv` |
| 08 | 비지도학습 | `KMeans`, `PCA`, 실루엣 | `cluster_result.csv`, `pca_2d.png` |
| 09 | 이미지 처리 | `cv2`(resize, gray, Canny, findContours), YOLOv5 | `rectangles.csv`, `detections.csv` |
| 10 | 이미지 분류·OCR·영상 | `Counter`, `easyocr`, `VideoCapture` | `object_count.csv`, `drone_detection.csv` |

## 세션별 핵심

### 01 결측치·이상치
- 결측: 삭제(`dropna`) / 대치(평균 `fillna(mean)`, 중앙값). 어떤 열을 평균·중앙값으로 채우라는 지시를 그대로 따를 것.
- 이상치: **Z-score > 3** 제거, 또는 **IQR**(Q1−1.5·IQR ~ Q3+1.5·IQR 밖).
- 센서 로그 통합: `merge(on="time")`, 문자열 `"error"` → `NaN`(`pd.to_numeric(errors="coerce")`) → 평균 대치 → `dropna`.

### 02 정규화·인코딩
- 표준화(평균0·표준편차1, `StandardScaler`) vs 정규화(0~1, `MinMaxScaler`). **문제에서 어느 쪽인지 지정함**.
- 라벨 인코딩(정수) vs 원핫(`get_dummies`). 순서 없는 범주는 원핫이 안전.
- 파일 경로 유효성: `df["path"].apply(os.path.exists)`로 `exists` 컬럼 → 필터링 → valid/missing 두 파일 저장.

### 03 시계열
- 순서: `pd.to_datetime` → `sort_values`/`set_index` → `resample('H').sum()`. 주기 코드: `min`, `H`, `D`, `W`, `M`, `Q`, `Y`.
- JSON 중첩(`items` 안의 water/ration/medicine) → `pd.json_normalize` 후 `rename`으로 컬럼명 정리.

### 04 기술통계량
- 평균·중앙값·최빈값·분산·표준편차·IQR·범위. `df.agg(["mean","median","std"])`, `groupby("unit").agg(...)`.
- 최빈값은 `mode()`가 Series를 반환(여러 개일 수 있음) → `.iloc[0]`.

### 05 시각화
- 히스토그램(분포), 박스플롯(이상치), 산점도(두 변수 관계), 상관계수 행렬+heatmap.
- 저장 폴더는 `os.makedirs(..., exist_ok=True)`, 저장은 `plt.savefig` 후 `plt.close()`.

### 06 데이터 해석
- 상관계수 해석: |r| 0.7↑ 강, 0.3~0.7 중간, 0.3↓ 약. 부호 = 방향.
- 임계치(예: 중앙값)로 높은/낮은 그룹을 나눠 평균 비교.
- `groupby().mean()`, `idxmin()`(가장 낮은 항목명), `pivot_table(index, values, aggfunc)`.
- 지표 방향 주의: `repair_freq`는 **낮을수록 우수**.

### 07 지도학습·평가
- 분류: 라벨 인코딩 → `train_test_split(test_size=0.2, random_state=42)` → `RandomForestClassifier` → `accuracy_score`, `confusion_matrix`, `classification_report`.
- 회귀: `LinearRegression` → RMSE(`mean_squared_error`의 제곱근) → 실제 vs 예측 그래프.
- 다중분류(A/B/C): `GradientBoostingClassifier`/`RandomForestClassifier`.
- 지표: 정확도·정밀도·재현율·F1(분류), MAE·MSE·RMSE·R²(회귀).

### 08 비지도학습
- `KMeans(n_clusters=3)` → `cluster` 컬럼 → `groupby("cluster").mean()`으로 군집 특성 해석.
- `StandardScaler` → `PCA(n_components=2)` → 산점도, `pca.components_`로 축 해석.
- 실루엣 계수(−1~1, 클수록 군집이 잘 분리됨)로 군집 수 비교.

### 09 이미지 처리 (OpenCV)
- 읽기·변환: `cv2.imread` → `cvtColor(BGR2GRAY)` → `resize((256,256))` → 평균 밝기 `gray.mean()`.
- 사각형 검출: `GaussianBlur` → `Canny` → `findContours` → `approxPolyDP(0.02*arcLength)` → 꼭짓점 4개 & `isContourConvex` → `boundingRect`.
- YOLOv5: `torch.hub.load('ultralytics/yolov5','yolov5s')` → `results.pandas().xyxy[0]`의 `name, xmin, ymin, xmax, ymax`.

### 10 이미지 분류·OCR·영상
- 폴더 순회: `[f for f in os.listdir(d) if f.lower().endswith(('.jpg','.png','.jpeg'))]`.
- 클래스 빈도: `collections.Counter` → 상위 3개 `most_common(3)` → 막대그래프.
- OCR: `easyocr.Reader(['ko','en']).readtext(img)` → 정규식(`re`)으로 한글·영문·숫자만 남김.
- 영상: `cv2.VideoCapture` → `isOpened()` → `read()` 루프, **FPS마다 1프레임**(`cap.get(cv2.CAP_PROP_FPS)`).

## 시험 대비 포인트
1. 모든 문제는 **파일명·컬럼명까지 지시대로** 저장(`index=False`). 지시한 이름이 틀리면 채점 불가.
2. 평가는 반드시 **분할 후**(테스트셋) 수행. 정규화는 분할 전/후 중 지시를 따르되 누수에 유의.
3. 해석 문제는 **숫자 근거 + 한두 문장**(주석 또는 마크다운 셀).
4. 시각화는 제목·축 라벨 포함, 저장 후 `plt.close()`.
5. 교육 자료에 **없는** 영역(텍스트 분류, 시계열 분류 모델)은 `../notebooks/` 참고.
