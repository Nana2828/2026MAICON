# 📚 시험용 통합 치트시트 (세션 01~10, 개념 → 문제 → 함수 → 코드)

> **수업 PPT 순서 그대로**, 세션마다 **① 간단 개념 → 지문 요점 → ② 함수 정리(뜻·언제) → ③ 코드 설명(줄마다 문법·과정 주석) → ④ 코드(복붙용)** 순서로 한 군데에 이어 놨습니다.  
> 시험 중에는 아래 **[지문 키워드로 찾기](#지문-키워드로-찾기)** 또는 **[목차](#목차)**에서 링크를 눌러 해당 문제로 이동하세요. 함수 이름이 생각나면 **[함수 빠른 찾기](#함수-빠른-찾기)**, 그냥 찾으려면 `Ctrl+F`.

> ⚠ **시험 환경은 Python 3.9 + pandas 1.x로 보입니다**(RMSE는 `np.sqrt(mean_squared_error)`, 리샘플링은 `"H"`). `scipy`/`sklearn`이 안 되면 pandas 직접 계산 방식(세션 01·02 코드 참고)을 쓰세요.  
> ⚠ **컬럼명은 지문과 실제 파일이 다를 수 있습니다** → 항상 `df.columns`로 확인.  
> ⚠ **임시로 만든 컬럼은 저장 전에 삭제**(문제에서 요구했으면 유지), 저장은 `index=False`, 파일명은 지문과 한 글자도 다르지 않게, 모델은 **분할 후 테스트셋으로 평가**.  

## 지문 키워드로 찾기

| 지문에 이런 말이 있으면 | 이렇게 한다 | 바로가기 |
|---|---|---|
| 빈칸 / 누락 / NaN | `fillna`(평균·중앙값) 또는 `dropna()` | [세션 01 문제 1](#01-1-정비-기록-결측치-처리) |
| 이상치 제거·탐지 | Z-score(3 초과) 또는 IQR(1.5배) | [세션 01 문제 2](#01-2-건강검진-이상치-제거) |
| 합쳐라 / 통합 / 병합 | `pd.merge(on=기준열)` | [세션 01 문제 3](#01-3-센서-로그-통합정제) |
| 정규화(0~1) / 표준화 | MinMaxScaler / StandardScaler | [세션 02 문제 1](#02-1-체력-측정-결과-정규화) |
| 문자 → 숫자 / 인코딩 | Label(정답열·순서) / One-Hot(순서 없는 입력) | [세션 02 문제 2](#02-2-보직지역-인코딩) |
| 파일 존재 / 경로 | `os.path.exists` → 필터 | [세션 02 문제 3](#02-3-영상-경로-유효성-검사) |
| 시간/일/주 단위 집계 | `to_datetime` → 정렬 → `resample` | [세션 03 문제 1](#03-1-센서-로그-시간대별-통계) |
| JSON | `json.load` → `json_normalize` → `rename` | [세션 03 문제 2](#03-2-보급-기록-json--csv) |
| 평균·중앙값·표준편차(그룹별) | `agg` / `groupby` | [세션 04 문제 1](#04-1-부대별-통계--장비-사용-분포--설문-요약) |
| 분포 / 이상치 그래프 | 히스토그램 / 박스플롯 | [세션 05 문제 1](#05-1-분포이상치--산점도상관--상관-heatmap) |
| 두 변수 관계 / 상관 | 산점도 / `corr` + heatmap | [세션 05 문제 1](#05-1-분포이상치--산점도상관--상관-heatmap) |
| ~별 평균, 표로 요약 | `groupby().mean()` / `pivot_table` | [세션 06 문제 1](#06-1-관계-해석--그룹-통계--운용-효율) |
| 정답이 범주(적합·A/B/C) → 분류 | RandomForestClassifier → 정확도·혼동행렬 | [세션 07 문제 1](#07-1-전투-적합도-분류) |
| 정답이 숫자(수명·점수) → 회귀 | LinearRegression/RandomForestRegressor → RMSE | [세션 07 문제 2](#07-2-장비-수명-예측회귀) |
| 3개 이상 클래스 | GradientBoostingClassifier + LabelEncoder | [세션 07 문제 3](#07-3-정비-시급성-다중분류) |
| 비슷한 것끼리 묶기 / 2차원 축소 | KMeans / PCA (먼저 표준화) | [세션 08 문제 1](#08-1-군집화--pca-2차원--근무-유형-군집) |
| 이미지 크기·흑백·밝기 | `cv2.resize` / `cvtColor` | [세션 09 문제 1](#09-1-이미지-밝기) |
| 사각형·윤곽 좌표 | Canny → findContours → approxPolyDP | [세션 09 문제 2](#09-2-설계도-사각형-검출) |
| 사람·차량 탐지(YOLO) | YOLO → 클래스별 집계 | [세션 09 문제 3](#09-3-객체-탐지yolo와-좌표-저장) |
| 객체 빈도 / 상위 N개 | `Counter.most_common` | [세션 10 문제 1](#10-1-객체-빈도-통계) |
| 이미지 속 글자(OCR) | EasyOCR + 정규식 | [세션 10 문제 2](#10-2-이미지-속-글자ocr) |
| 영상 프레임 | `VideoCapture`, `i % fps == 0` | [세션 10 문제 3](#10-3-드론-영상-프레임-탐지) |
| 한글이 깨짐 / csv 읽기·저장 | 읽기는 인코딩 폴백, 저장은 기본 utf-8(필요 시 utf-8-sig) | [한글·인코딩](#한글인코딩-깨짐-방지) |

## 시험 당일 체크리스트 (참가자 예선 가이드)

출처: 2026 국방 AI 경진대회 **참가자 예선 가이드**(쪽 번호는 가이드 PDF 기준).

| 항목 | 내용 |
|---|---|
| 일정 | **10/10(토)**. 입실 버튼 13:00 활성, **응시는 14:00부터**. 시험 시작 가능 시간 14:00~16:30 (p.6, 14, 25) |
| 시간 | 시작부터 **90분**. 단 **16:30에 일괄 자동 종료**(예: 15:30 시작이면 60분뿐) → **늦어도 15:00 전에 시작**해야 90분을 다 씀. 입실은 PC 시간이 아니라 화면의 **서버 시간** 기준 (p.25) |
| 문항 | 3문항, Jupyter Notebook, **Python3만**(R·다른 언어는 우수자 선발 제외). **문항 순서와 상관없이** 풀 수 있음 (p.9, 22, 28) |
| 배점 | 문항1 **20점**(중상), 문항2 **35점**(상), 문항3 **45점**(최상). **동점이면 제출 시간이 빠를수록 유리** (p.26) |
| 화면 버튼 | **도움말**(풀이 전 필독), **초기화**(문제와 답안이 **전부 삭제**되니 누르지 말 것), **저장**(`.ipynb`), **데이터 검증**(정답 csv가 정해진 위치에 있는지 확인, 제출이 아님), **최종 제출 및 테스트 종료**(**1회만**, 안 누르면 미제출) (p.19) |
| 저장 | 시험 도중 **반드시 저장 버튼**으로 `.ipynb` 저장. 페이지를 이탈하면 저장 안 한 코드는 소실. 창이 닫혀도 **시간은 계속 흐름**(다시 접속 가능) (p.15, 23) |
| 환경 | 최신 Chrome 권장(엣지·웨일 가능), Windows 10 이상/8GB RAM/업로드 5Mbps 이상/해상도 1280*720, 충전기 준비, **공용 네트워크(카페·도서관) 금지**, **가상 PC·원격 접속 프로그램 금지**, 마우스·키보드 외 입력 도구(터치) 금지 (p.12, 16) |
| 결과 발표 | 10/16 (변동 가능) (p.9) |

**금지 행위 (p.16, 23, 24)** — 적발되면 응시 무효·차기 대회 참여 제한(1회 소명), 법적 책임까지 가능
- **문제 내용의 전체 또는 일부를 캡처하거나 복사**하는 행위, 시험 정보·답안을 인터넷에 게시하거나 타인에게 공유
- 제공 **소스코드·데이터의 다운로드 및 외부 저장**, **클라우드 자동 업로드**(OneDrive 등), 원격제어, **화면 공유**
- 타인과 **공동 문제 풀이**, 실시간 화면 공유, **실시간 코딩 대리 요청**
- 크롤링, 자동화 봇 사용, 내부 API 무단 호출
- 같은 계정으로 **여러 IP에서 동시 접속**, **다중 동시 작업**
- 타인 코드·사업용 코드의 무단 사용

**AI 보조 도구 (p.23)**
- 가이드: "AI 등 보조 도구 사용은 가능하지만, 단순 복사/붙여넣기를 할 경우 부정확하거나 비정상적인 결과가 나올 수 있습니다. 따라서 **AI 도구 사용으로 발생하는 모든 결과는 본인에게 책임**이 있습니다."
- 그러나 **문제 내용을 복사하는 것 자체가 금지(p.16)**이므로, AI에는 **문제와 상관없이 일반화한 질문**(함수 사용법, 개념, 오류 해석)만 하고, 받은 코드는 직접 읽고 내 노트북에 **직접 타이핑**해서 내 문제에 맞게 바꿉니다.

**전략 제안**
- 문항3이 45점으로 가장 크지만 가장 어렵습니다. **쉬운 문항부터 결과 csv를 먼저 저장**하고, 막히는 문항은 건너뛰었다가 돌아옵니다(순서 무관).
- 문항마다 **일단 베이스라인 csv를 저장** → '데이터 검증'으로 위치 확인 → 시간이 남으면 개선.
- 끝나기 전에 반드시 **저장 → 데이터 검증 → 최종 제출 및 테스트 종료**.


## 목차

- [세션 01. 결측치·이상치 처리](#세션-01-결측치이상치-처리)  
  - [01-1. 정비 기록 결측치 처리](#01-1-정비-기록-결측치-처리)
  - [01-2. 건강검진 이상치 제거](#01-2-건강검진-이상치-제거)
  - [01-3. 센서 로그 통합·정제](#01-3-센서-로그-통합정제)
- [세션 02. 정규화·인코딩](#세션-02-정규화인코딩)  
  - [02-1. 체력 측정 결과 정규화](#02-1-체력-측정-결과-정규화)
  - [02-2. 보직·지역 인코딩](#02-2-보직지역-인코딩)
  - [02-3. 영상 경로 유효성 검사](#02-3-영상-경로-유효성-검사)
- [세션 03. 시계열 정렬·리샘플링 / JSON](#세션-03-시계열-정렬리샘플링--json)  
  - [03-1. 센서 로그 시간대별 통계](#03-1-센서-로그-시간대별-통계)
  - [03-2. 보급 기록 JSON → CSV](#03-2-보급-기록-json--csv)
- [세션 04. 기술통계량](#세션-04-기술통계량)  
  - [04-1. 부대별 통계 / 장비 사용 분포 / 설문 요약](#04-1-부대별-통계--장비-사용-분포--설문-요약)
- [세션 05. 데이터 시각화](#세션-05-데이터-시각화)  
  - [05-1. 분포·이상치 / 산점도·상관 / 상관 heatmap](#05-1-분포이상치--산점도상관--상관-heatmap)
- [세션 06. 데이터 해석](#세션-06-데이터-해석)  
  - [06-1. 관계 해석 / 그룹 통계 / 운용 효율](#06-1-관계-해석--그룹-통계--운용-효율)
- [세션 07. 지도학습 및 평가](#세션-07-지도학습-및-평가)  
  - [07-1. 전투 적합도 분류](#07-1-전투-적합도-분류)
  - [07-2. 장비 수명 예측(회귀)](#07-2-장비-수명-예측회귀)
  - [07-3. 정비 시급성 다중분류](#07-3-정비-시급성-다중분류)
- [세션 08. 비지도학습](#세션-08-비지도학습)  
  - [08-1. 군집화 / PCA 2차원 / 근무 유형 군집](#08-1-군집화--pca-2차원--근무-유형-군집)
- [세션 09. 이미지 처리 (OpenCV)](#세션-09-이미지-처리-opencv)  
  - [09-1. 이미지 밝기](#09-1-이미지-밝기)
  - [09-2. 설계도 사각형 검출](#09-2-설계도-사각형-검출)
  - [09-3. 객체 탐지(YOLO)와 좌표 저장](#09-3-객체-탐지yolo와-좌표-저장)
- [세션 10. 이미지 분류·OCR·영상](#세션-10-이미지-분류ocr영상)  
  - [10-1. 객체 빈도 통계](#10-1-객체-빈도-통계)
  - [10-2. 이미지 속 글자(OCR)](#10-2-이미지-속-글자ocr)
  - [10-3. 드론 영상 프레임 탐지](#10-3-드론-영상-프레임-탐지)
- [종합문제 대비 (세션 11·12)](#종합문제-대비-세션-1112)
- [한글·인코딩 (깨짐 방지)](#한글인코딩-깨짐-방지)
- [시험 당일 체크리스트 (참가자 예선 가이드)](#시험-당일-체크리스트-참가자-예선-가이드)
- [공통 시작 코드](#공통-시작-코드)

## 함수 빠른 찾기

함수 이름을 눌러 설명과 코드가 있는 곳으로 이동합니다.

[`pd.read_csv() / df.to_csv()`](#01-1-정비-기록-결측치-처리) · [`df.head() / df.describe()`](#01-1-정비-기록-결측치-처리) · [`df['컬럼']`](#01-1-정비-기록-결측치-처리) · [`fillna(값)`](#01-1-정비-기록-결측치-처리) · [`Series.mean() / median() / std()`](#01-1-정비-기록-결측치-처리) · [`scipy.stats.zscore`](#01-2-건강검진-이상치-제거) · [`df[조건식]`](#01-2-건강검진-이상치-제거) · [`apply()`](#01-2-건강검진-이상치-제거) · [`drop()`](#01-2-건강검진-이상치-제거) · [`pd.merge(a, b, on=, suffixes=)`](#01-3-센서-로그-통합정제) · [`dropna()`](#01-3-센서-로그-통합정제) · [`MinMaxScaler().fit_transform()`](#02-1-체력-측정-결과-정규화) · [`pd.DataFrame(배열, columns=)`](#02-1-체력-측정-결과-정규화) · [`pd.concat([a, b], axis=1)`](#02-1-체력-측정-결과-정규화) · [`Series.min() / max()`](#02-1-체력-측정-결과-정규화) · [`LabelEncoder()`](#02-2-보직지역-인코딩) · [`pd.get_dummies(df, columns=)`](#02-2-보직지역-인코딩) · [`dict() / list() / zip()`](#02-2-보직지역-인코딩) · [`lambda 입력: 식`](#02-3-영상-경로-유효성-검사) · [`os.path.exists(경로)`](#02-3-영상-경로-유효성-검사) · [`pd.to_datetime()`](#03-1-센서-로그-시간대별-통계) · [`sort_values() / set_index()`](#03-1-센서-로그-시간대별-통계) · [`resample('H').sum()`](#03-1-센서-로그-시간대별-통계) · [`plt.title/xlabel/ylabel/grid/tight_layout/savefig`](#03-1-센서-로그-시간대별-통계) · [`with open() / json.load()`](#03-2-보급-기록-json--csv) · [`pd.json_normalize()`](#03-2-보급-기록-json--csv) · [`df.rename(columns={})`](#03-2-보급-기록-json--csv) · [`df.agg([...])`](#04-1-부대별-통계--장비-사용-분포--설문-요약) · [`mode() / var() / quantile()`](#04-1-부대별-통계--장비-사용-분포--설문-요약) · [`str.strip() / '구분자'.join()`](#04-1-부대별-통계--장비-사용-분포--설문-요약) · [`Series.to_frame() / df.T`](#04-1-부대별-통계--장비-사용-분포--설문-요약) · [`iloc[] / loc[]`](#04-1-부대별-통계--장비-사용-분포--설문-요약) · [`os.makedirs(폴더, exist_ok=True)`](#05-1-분포이상치--산점도상관--상관-heatmap) · [`plt.subplot() / plt.subplots()`](#05-1-분포이상치--산점도상관--상관-heatmap) · [`plt.hist() / plt.boxplot()`](#05-1-분포이상치--산점도상관--상관-heatmap) · [`sns.scatterplot() / plt.legend()`](#05-1-분포이상치--산점도상관--상관-heatmap) · [`df.corr() / sns.heatmap(annot=True)`](#05-1-분포이상치--산점도상관--상관-heatmap) · [`round(값, 자리)`](#06-1-관계-해석--그룹-통계--운용-효율) · [`임계치(threshold)로 그룹 나누기`](#06-1-관계-해석--그룹-통계--운용-효율) · [`groupby().mean()`](#06-1-관계-해석--그룹-통계--운용-효율) · [`Series.idxmin() / idxmax()`](#06-1-관계-해석--그룹-통계--운용-효율) · [`pd.pivot_table(df, index, values, aggfunc)`](#06-1-관계-해석--그룹-통계--운용-효율) · [`train_test_split()`](#07-1-전투-적합도-분류) · [`RandomForestClassifier / fit / predict`](#07-1-전투-적합도-분류) · [`accuracy_score / confusion_matrix / classification_report`](#07-1-전투-적합도-분류) · [`LinearRegression`](#07-2-장비-수명-예측회귀) · [`mean_squared_error → RMSE`](#07-2-장비-수명-예측회귀) · [`GradientBoostingClassifier`](#07-3-정비-시급성-다중분류) · [`KMeans(n_clusters=3)`](#08-1-군집화--pca-2차원--근무-유형-군집) · [`PCA(n_components=2) / pca.components_`](#08-1-군집화--pca-2차원--근무-유형-군집) · [`silhouette_score`](#08-1-군집화--pca-2차원--근무-유형-군집) · [`cv2.imread(경로)`](#09-1-이미지-밝기) · [`cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`](#09-1-이미지-밝기) · [`cv2.resize(img, (256, 256))`](#09-1-이미지-밝기) · [`cv2.GaussianBlur(img, (5,5), 0)`](#09-2-설계도-사각형-검출) · [`cv2.Canny(img, 50, 150)`](#09-2-설계도-사각형-검출) · [`cv2.findContours(...)`](#09-2-설계도-사각형-검출) · [`cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)`](#09-2-설계도-사각형-검출) · [`cv2.isContourConvex(ap)`](#09-2-설계도-사각형-검출) · [`cv2.boundingRect(ap)`](#09-2-설계도-사각형-검출) · [`PIL.Image.open(경로)`](#09-3-객체-탐지yolo와-좌표-저장) · [`torch.hub.load('ultralytics/yolov5','yolov5s', pretrained=True)`](#09-3-객체-탐지yolo와-좌표-저장) · [`results.pandas().xyxy[0]`](#09-3-객체-탐지yolo와-좌표-저장) · [`[f for f in os.listdir(d) if f.lower().endswith(('.jpg','.png','.jpeg'))]`](#10-1-객체-빈도-통계) · [`collections.Counter(리스트)` / `.most_common(3)`](#10-1-객체-빈도-통계) · [`easyocr.Reader(['ko','en'])` / `readtext(경로)`](#10-2-이미지-속-글자ocr) · [`re.match(r'^[가-힣A-Za-z0-9]+$', text)`](#10-2-이미지-속-글자ocr) · [`cv2.VideoCapture(경로)` / `isOpened()` / `read()`](#10-3-드론-영상-프레임-탐지) · [`cap.get(cv2.CAP_PROP_FPS)`](#10-3-드론-영상-프레임-탐지)


---

## 세션 01. 결측치·이상치 처리  
[↑ 목차](#목차)

**① 간단 개념 (세션 01)**

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

### 01-1. 정비 기록 결측치 처리  
[↑ 세션 01](#세션-01-결측치이상치-처리)

**지문 요점**

1. `repair_count`, `repair_duration` 빈칸 → 각 열의 **평균**으로
2. `last_check_day` 빈칸 → **중앙값**으로
3. `maintenance_cleaned.csv`로 저장

**② 함수 정리 (PPT '활용 코드 정리')**

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

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 읽기 → 빈칸을 열별로 채우기 → 저장
df = pd.read_csv("파일.csv")
# 문법: pd.read_csv("경로") = csv를 표(DataFrame)로 읽는다. df는 그 표의 이름.

m = df["col_a"].mean()
# 문법: df["열이름"] = 열 하나(Series). .mean() = 그 열의 평균. NaN(빈칸)은 계산에서 빠진다.
# 과정: 채울 값을 먼저 변수에 담아 둔다. 안 그러면 채운 뒤 평균이 달라진다.

df["col_a"] = df["col_a"].fillna(m)
# 문법: .fillna(값) = NaN을 값으로 채운 "새 열"을 돌려준다. 원본이 자동으로 바뀌지는 않는다.
# 문법: df["col_a"] = ... 로 다시 넣어야 표에 반영된다. (이 대입을 빼먹는 실수가 많다)

df["col_b"] = df["col_b"].fillna(df["col_b"].median())
# 문법: .median() = 중앙값. 지문이 "중앙값으로"라고 하면 mean 대신 이것.
# 과정: 열마다 지문이 정한 값(평균/중앙값)으로 한 줄씩 반복한다.

df.to_csv("결과.csv", index=False)
# 문법: .to_csv("파일명") = 표를 csv로 저장. index=False = 0,1,2… 번호 열은 쓰지 않는다.
```

**④ 코드**

```python
df = pd.read_csv("maintenance_log.csv")
df["repair_count"] = df["repair_count"].fillna(df["repair_count"].mean())
df["repair_duration"] = df["repair_duration"].fillna(df["repair_duration"].mean())
df["last_check_day"] = df["last_check_day"].fillna(df["last_check_day"].median())
df.to_csv("maintenance_cleaned.csv", index=False)
```

### 01-2. 건강검진 이상치 제거  
[↑ 세션 01](#세션-01-결측치이상치-처리)

**지문 요점**

1. `bmi`, `blood_pressure`에서 **Z-score 3 초과**를 이상치로 보고 제거
2. `health_clean.csv`로 저장
3. **제거된 행 수 출력**

**② 함수 정리 (PPT '활용 코드 정리')**

- `scipy.stats.zscore` — 표준점수(Z). 절댓값 3 초과=이상치  
  ↳ **언제**: "Z-score로 이상치". scipy가 안 되면 `(x-x.mean())/x.std(ddof=0)`.
- `df[조건식]` — 조건에 맞는 행만 선택  
  ↳ **언제**: "~인 행만 남겨라/골라라". 조건 여러 개는 `(a) & (b)`, `|`로 묶고 각각 괄호.
- `apply()` — 각 열/값에 함수 적용  
  ↳ **언제**: 각 열/값에 함수를 한꺼번에 적용할 때(예: 열마다 zscore).
- `drop()` — 행/열 삭제  
  ↳ **언제**: 열을 지울 때 `columns=[...]`, 행을 지울 때 `index=[...]`. 임시 컬럼 정리에 사용.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 열별 Z-score 계산 → 기준 넘는 행 찾기 → 제거 → 개수 출력 → 저장
cols = ["col_a", "col_b"]
# 문법: 열 이름 리스트. 한 번 정의해 두면 아래에서 반복해 쓴다.

z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
# 문법: df[cols] = 여러 열을 고르면 표(대괄호 2개). 표 - 평균 = 열마다 자기 평균을 뺀다.
# 문법: .std(ddof=0) = 모표준편차. scipy의 zscore와 같은 값을 얻으려면 ddof=0.
# 과정: Z = (값 - 평균) / 표준편차. 평균에서 표준편차의 몇 배 떨어졌는지.

mask = (z.abs() <= 3).all(axis=1)
# 문법: z.abs() = 절댓값. <= 3 = 각 칸이 True/False. .all(axis=1) = 한 행에서 "모두 True"일 때만 True.
# 과정: 지문이 "3 초과를 이상치"라 했으니 3 이하인 행만 정상. 열이 여러 개면 한 열이라도 넘으면 그 행은 제거.

print("제거된 행 수:", (~mask).sum())
# 문법: ~mask = True/False 뒤집기. True는 1로 세어지므로 .sum() = 제거 대상 개수.

clean = df[mask]
# 문법: df[True/False 열] = True인 행만 남긴다. (불리언 인덱싱)

clean.to_csv("결과.csv", index=False)
# 과정: 계산하려고 만든 임시 열이 있으면 저장 전에 drop(columns=[...])으로 지운다.

# ── IQR 방식 (지문이 IQR/사분위라고 할 때) ──
q1, q3 = df["col_a"].quantile([.25, .75])
# 문법: .quantile([.25, .75]) = 25%, 75% 지점 값을 한 번에. 앞의 값은 q1, 뒤의 값은 q3에 나눠 담는다.
iqr = q3 - q1
df_iqr = df[df["col_a"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]
# 문법: .between(하한, 상한) = 하한~상한 사이면 True (양 끝 포함).
# 과정: 정상 범위 = Q1-1.5·IQR ~ Q3+1.5·IQR. 이 범위 안의 행만 남긴다.
```

**④ 코드**

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
z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
mask = (z.abs() <= 3).all(axis=1)
print("제거된 행 수:", (~mask).sum())
clean = df[mask]; clean.to_csv("health_clean.csv", index=False)

q1, q3 = df["bmi"].quantile([.25, .75]); iqr = q3 - q1
df_iqr = df[df["bmi"].between(q1 - 1.5*iqr, q3 + 1.5*iqr)]
```

### 01-3. 센서 로그 통합·정제  
[↑ 세션 01](#세션-01-결측치이상치-처리)

**지문 요점**

1. 두 센서 파일을 **시간 기준으로 병합**
2. `motion_count`의 `"error"` → 결측 → 전체 **평균**으로 대체
3. 남은 결측 행 제거 후 `merged_sensor_cleaned.csv` 저장

**② 함수 정리 (PPT '활용 코드 정리')**

- `pd.merge(a, b, on=, suffixes=)` — 두 표를 기준 열로 합치기. 겹치는 열 이름 구분  
  ↳ **언제**: 파일/표가 두 개 이상이고 "합쳐라". 기준 열이 같아야 하고 겹치는 열은 `suffixes`로 구분.
- `dropna()` — 빈칸이 있는 행 삭제  
  ↳ **언제**: "빈칸 있는 행은 제거". 특정 열만 보려면 `subset=[...]`.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 두 파일 읽기 → 기준 열로 합치기 → 문자 "error"를 NaN으로 → 평균으로 채우기 → 남은 빈칸 행 삭제 → 저장
a = pd.read_csv("a.csv"); b = pd.read_csv("b.csv")
# 문법: 한 줄에 `;`로 두 문장을 쓸 수 있다.

merged = pd.merge(a, b, on=["time", "post_id"], how="inner")
# 문법: pd.merge(왼쪽표, 오른쪽표, on=기준열, how=방식). on에 리스트를 주면 여러 열이 모두 같은 행끼리 합친다.
# 문법: how="inner" = 양쪽에 모두 있는 행만. "left" = 왼쪽 표의 행은 전부 유지(없는 쪽은 NaN).
# 과정: 기준 열 이름·값이 두 표에서 같아야 합쳐진다. 겹치는 다른 열은 suffixes=("_a","_b")로 구분.

merged["col"] = pd.to_numeric(merged["col"], errors="coerce")
# 문법: pd.to_numeric(열, errors="coerce") = 숫자로 바꾸고, 못 바꾸는 값("error" 같은 글자)은 NaN으로 만든다.
# 과정: 이걸 해야 "error"가 섞인 열이 숫자 열이 되어 평균 계산이 가능하다.

merged["col"] = merged["col"].fillna(merged["col"].mean())
# 과정: 지문이 "평균으로 대체"라고 했으니 NaN을 평균으로 채운다.

merged = merged.dropna()
# 문법: .dropna() = NaN이 하나라도 있는 행을 삭제. 특정 열만 보려면 dropna(subset=["col"]).

merged.to_csv("결과.csv", index=False)
```

**④ 코드**

```python
m = pd.read_csv("motion_sensor.csv"); t = pd.read_csv("temp_sensor.csv")
merged = pd.merge(m, t, on=["time", "post_id"], how="inner")
merged["motion_count"] = pd.to_numeric(merged["motion_count"], errors="coerce")
merged["motion_count"] = merged["motion_count"].fillna(merged["motion_count"].mean())
merged = merged.dropna()
merged.to_csv("merged_sensor_cleaned.csv", index=False)
```


---

## 세션 02. 정규화·인코딩  
[↑ 목차](#목차)

**① 간단 개념 (세션 02)**

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

### 02-1. 체력 측정 결과 정규화  
[↑ 세션 02](#세션-02-정규화인코딩)

**지문 요점**

1. `pushup_count`, `run_time_2km`, `situp_count`에 **MinMaxScaler**
2. **원본과 함께** `fitness_scaled.csv` 저장
3. 각 컬럼의 **최소/최대값 출력**

**② 함수 정리 (PPT '활용 코드 정리')**

- `MinMaxScaler().fit_transform()` — 0~1 정규화  
  ↳ **언제**: "0~1 정규화". 값의 범위가 중요할 때.
- `pd.DataFrame(배열, columns=)` — 배열을 표로 만들기  
  ↳ **언제**: 스케일러 결과(배열)를 다시 표로 만들 때. 열 이름을 꼭 지정.
- `pd.concat([a, b], axis=1)` — 표 이어붙이기(axis=1 옆으로, 0 아래로)  
  ↳ **언제**: 원본 표 옆에 새 열(정규화 결과 등)을 붙일 때(axis=1). 행을 아래로 이으려면 axis=0.
- `Series.min() / max()` — 최솟값 / 최댓값  
  ↳ **언제**: 정규화 결과 범위 확인(0~1인지), 값 범위 점검.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 정규화할 열 고르기 → 스케일러 적용 → 새 열 이름 붙여 표로 만들기 → 원본 옆에 붙이기 → 저장
from sklearn.preprocessing import MinMaxScaler
# 문법: from 모듈 import 이름 = 모듈에서 필요한 것만 가져온다.

cols = ["col_a", "col_b", "col_c"]
# 과정: 지문이 정규화하라고 한 열만 리스트에 넣는다. 열 이름은 df.columns로 확인.

arr = MinMaxScaler().fit_transform(df[cols])
# 문법: MinMaxScaler() = 스케일러 만들기. .fit_transform(표) = 최솟값·최댓값을 배운(fit) 뒤 바로 변환(transform).
# 과정: 변환식 (x - min) / (max - min) → 모든 값이 0~1. 결과는 표가 아니라 숫자 배열(numpy)이다.

scaled = pd.DataFrame(arr, columns=[c + "_scaled" for c in cols])
# 문법: pd.DataFrame(배열, columns=열이름들) = 배열을 표로 되돌린다.
# 문법: [c + "_scaled" for c in cols] = 리스트 컴프리헨션. cols의 각 이름 뒤에 "_scaled"를 붙인 새 리스트.
# 과정: 열 이름을 지정하지 않으면 0,1,2로 나온다.

out = pd.concat([df, scaled], axis=1)
# 문법: pd.concat([표1, 표2], axis=1) = 옆으로 붙인다. (axis=0은 아래로)
# 주의: axis=1은 "행 번호(인덱스)가 같은 것끼리" 붙는다. df와 scaled의 행 번호가 같아야 한다.

out.to_csv("결과.csv", index=False)
print(scaled.min(), scaled.max())
# 과정: 각 열의 최솟값이 0, 최댓값이 1인지 확인하는 출력. StandardScaler는 평균 0, 표준편차 1.
```

**④ 코드**

```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler
df = pd.read_csv("fitness_test.csv")
cols = ["pushup_count", "run_time_2km", "situp_count"]
scaled = pd.DataFrame(MinMaxScaler().fit_transform(df[cols]), columns=[c + "_scaled" for c in cols])
out = pd.concat([df, scaled], axis=1); out.to_csv("fitness_scaled.csv", index=False)
print(scaled.min(), scaled.max())
```

### 02-2. 보직·지역 인코딩  
[↑ 세션 02](#세션-02-정규화인코딩)

**지문 요점**

1. `position` → **Label Encoding**, `region` → **One-Hot**
2. `encoded_soldiers.csv` 저장
3. 각 인코딩 컬럼의 **설명 출력**

**② 함수 정리 (PPT '활용 코드 정리')**

- `LabelEncoder()` — 문자 범주를 정수로  
  ↳ **언제**: 타깃/순서 있는 범주를 정수로. 변환표는 `classes_`로 확인("인코딩 설명 출력").
- `pd.get_dummies(df, columns=)` — 원핫 인코딩  
  ↳ **언제**: 순서 없는 범주(지역 등)를 입력 특성으로 쓸 때. 열이 늘어난다.
- `dict() / list() / zip()` — 딕셔너리·리스트 만들기, 두 목록 짝짓기  
  ↳ **언제**: 인코딩 대응표를 출력하거나 두 목록을 짝지을 때.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 라벨 인코딩(한 열) → 대응표 출력 → 원핫(다른 열) → 저장
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
# 문법: LabelEncoder() = 글자 → 정수로 바꾸는 도구를 만든다.

df["col_enc"] = le.fit_transform(df["col_text"])
# 문법: .fit_transform(열) = 어떤 값들이 있는지 배우고(fit) 각 값을 정수로 바꾼다(transform). 알파벳/가나다 순으로 0,1,2…

print(dict(zip(le.classes_, le.transform(le.classes_))))
# 문법: le.classes_ = 배운 원래 값 목록. le.transform(...) = 그 값들의 정수.
# 문법: zip(a, b) = 두 목록을 짝지음. dict(...) = {원래값: 정수} 사전. 지문의 "인코딩 설명 출력"에 해당.

df = pd.get_dummies(df, columns=["col_cat"], dtype=int)
# 문법: pd.get_dummies(표, columns=[열]) = 그 열의 값마다 0/1 열을 새로 만들고 원래 열은 없앤다.
# 문법: dtype=int = True/False 대신 1/0으로. (이걸 빼면 True/False로 저장될 수 있다)
# 과정: 순서가 없는 범주(지역 등)는 원핫, 지문이 Label이라고 한 열은 LabelEncoder.

df.to_csv("결과.csv", index=False)
```

**④ 코드**

```python
from sklearn.preprocessing import LabelEncoder
df = pd.read_csv("soldier_info.csv")
le = LabelEncoder(); df["position_enc"] = le.fit_transform(df["position"])
print(dict(zip(le.classes_, le.transform(le.classes_))))
df = pd.get_dummies(df, columns=["region"], dtype=int)
df.to_csv("encoded_soldiers.csv", index=False)
```

### 02-3. 영상 경로 유효성 검사  
[↑ 세션 02](#세션-02-정규화인코딩)

**지문 요점**

1. `file_path`에 **실제 존재하는 파일만** 필터링
2. `exists`(True/False) 컬럼 추가
3. 있는 것 `valid_videos.csv`, 없는 것 `missing_videos.csv`로 저장

**② 함수 정리 (PPT '활용 코드 정리')**

- `lambda 입력: 식` — 이름 없는 짧은 함수  
  ↳ **언제**: `apply` 안에서 한 줄짜리 간단한 처리를 할 때.
- `os.path.exists(경로)` — 파일이 있는지 True/False  
  ↳ **언제**: 파일/폴더가 실제로 있는지 확인할 때.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 경로 열로 True/False 열 만들기 → 있는 것/없는 것으로 나눠 각각 저장
df["exists"] = df["file_path"].apply(lambda p: os.path.exists(p))
# 문법: .apply(함수) = 열의 값을 하나씩 함수에 넣어 결과를 모은다.
# 문법: lambda p: 식 = 이름 없는 한 줄 함수. p는 각 칸의 값(경로).
# 문법: os.path.exists(경로) = 그 경로에 파일/폴더가 있으면 True. (import os 필요)

df[df["exists"]].to_csv("valid.csv", index=False)
# 문법: df[True/False 열] = True인 행만. → 존재하는 것만 저장.

df[~df["exists"]].to_csv("missing.csv", index=False)
# 문법: ~ = True/False 뒤집기 → 존재하지 않는 것만 저장.
# 주의: 경로가 상대경로면 노트북 위치 기준이다. 파일 위치가 다르면 전부 False로 나온다.
```

**④ 코드**

```python
df = pd.read_csv("video_metadata.csv")
df["exists"] = df["file_path"].apply(lambda p: os.path.exists(p))
df[df["exists"]].to_csv("valid_videos.csv", index=False)
df[~df["exists"]].to_csv("missing_videos.csv", index=False)
```


---

## 세션 03. 시계열 정렬·리샘플링 / JSON  
[↑ 목차](#목차)

**① 간단 개념 (세션 03)**

**시계열 데이터**: 시간의 흐름에 따라 순서대로 기록된 데이터. 시간 정보(날짜·시각)가 있고 그에 따라 값이 변한다.
- 특징: **시간 종속성**, **추세(Trend)**, **계절성(Seasonality)**, **불규칙성(Irregularity)**
- 리샘플링 주기: 분 `min`, 시간 `H`, 일 `D`, 주 `W`, 월 `M`, 분기 `Q`, 연도 `Y`/`A`
- JSON → 표: `json.load` → `json_normalize` → `rename`

### 03-1. 센서 로그 시간대별 통계  
[↑ 세션 03](#세션-03-시계열-정렬리샘플링--json)

**지문 요점**

1. `timestamp`를 datetime으로 바꾸고 **정렬**
2. 감지 횟수를 **1시간 단위 합계**로 리샘플링
3. `hourly_motion.csv` 저장 + **시계열 그래프**

**② 함수 정리 (PPT '활용 코드 정리')**

- `pd.to_datetime()` — 문자를 날짜 형식으로  
  ↳ **언제**: 날짜가 문자열일 때 반드시 먼저 변환(정렬·리샘플링 전제).
- `sort_values() / set_index()` — 정렬 / 열을 인덱스로(inplace=True면 원본 변경)  
  ↳ **언제**: 시간순 정렬 후 날짜를 인덱스로 둬야 `resample`이 된다.
- `resample('H').sum()` — 시간 단위로 묶어 집계. 주기: min,H,D,W,M,Q,Y  
  ↳ **언제**: "시간/일/주 단위로 합계(sum)·평균(mean)". 지문의 단위에 맞게 주기를 고른다.
- `plt.title/xlabel/ylabel/grid/tight_layout/savefig` — 제목·축·격자·여백·저장  
  ↳ **언제**: 모든 그래프의 마무리. 저장 후 `plt.close()`.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 날짜 변환 → 시간순 정렬 → 날짜를 인덱스로 → 1시간 단위 합계 → 저장·그래프
df["timestamp"] = pd.to_datetime(df["timestamp"])
# 문법: pd.to_datetime(열) = 글자로 된 날짜·시각을 진짜 날짜 형식으로 바꾼다. 이걸 해야 시간 계산이 된다.

df = df.sort_values("timestamp").set_index("timestamp")
# 문법: .sort_values("열") = 그 열 기준 오름차순 정렬. .set_index("열") = 그 열을 행 이름(인덱스)으로.
# 문법: 점(.)으로 이어 쓰기 = 앞의 결과에 바로 다음 함수를 적용(메서드 체이닝).
# 과정: resample은 날짜가 인덱스일 때만 쓸 수 있다.

hourly = df["col"].resample("H").sum()
# 문법: .resample("H") = 1시간 단위로 묶는다. 뒤에 집계(.sum() 합계, .mean() 평균, .count() 개수)를 붙여야 한다.
# 문법: 주기 코드 "min" 분 / "H" 시간 / "D" 일 / "W" 주 / "M" 월.
# 과정: 지문이 "시간별 합계"면 sum, "시간별 평균"이면 mean.

hourly.to_csv("결과.csv")
# 주의: hourly는 인덱스(시간)가 중요한 데이터라 index=False를 쓰지 않는다. (시간 열이 사라진다)

plt.figure(figsize=(10, 4)); plt.plot(hourly.index, hourly.values)
# 문법: plt.figure(figsize=(가로, 세로)) = 그림 크기. plt.plot(x, y) = 선 그래프.
plt.title("제목"); plt.xlabel("x"); plt.ylabel("y"); plt.grid(True)
plt.tight_layout(); plt.savefig("그래프.png"); plt.close()
# 문법: tight_layout = 글자 잘림 방지. savefig = 파일 저장(show보다 먼저). close = 그림 닫기.
```

**④ 코드**

```python
df = pd.read_csv("sensor_log.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").set_index("timestamp")
hourly = df["motion_detected"].resample("H").sum()
hourly.to_csv("hourly_motion.csv")
plt.figure(figsize=(10, 4)); plt.plot(hourly.index, hourly.values)
plt.title("Hourly motion"); plt.xlabel("time"); plt.ylabel("sum"); plt.grid(True)
plt.tight_layout(); plt.savefig("hourly_motion.png"); plt.close()
```

### 03-2. 보급 기록 JSON → CSV  
[↑ 세션 03](#세션-03-시계열-정렬리샘플링--json)

**지문 요점**

1. JSON을 `unit, supply_date, water, ration, medicine` 컬럼의 DataFrame으로
2. `supply_log.csv` 저장
3. 항목별 **총합 출력**

**② 함수 정리 (PPT '활용 코드 정리')**

- `with open() / json.load()` — JSON 파일 읽기  
  ↳ **언제**: `.json` 파일을 파이썬 객체로 읽을 때.
- `pd.json_normalize()` — 중첩 JSON을 표로  
  ↳ **언제**: 중첩된 JSON(안에 딕셔너리)을 한 줄 표로 펼칠 때.
- `df.rename(columns={})` — 열 이름 바꾸기  
  ↳ **언제**: 열 이름을 지문이 요구한 이름으로 바꿀 때.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: JSON 파일 열기 → 파이썬 객체로 읽기 → 표로 펼치기 → 열 이름 정리 → 저장·합계
import json
with open("파일.json", encoding="utf-8") as f:
    data = json.load(f)
# 문법: with open(경로) as f: = 파일을 열고, 블록이 끝나면 자동으로 닫는다.
# 문법: json.load(f) = JSON을 리스트/딕셔너리로 읽는다. encoding="utf-8"로 한글 깨짐 방지.

df = pd.json_normalize(data)
# 문법: pd.json_normalize(데이터) = 안에 들어 있는 딕셔너리를 펼쳐 한 줄짜리 표로 만든다.
# 과정: {"items": {"water": 3}} 는 "items.water"라는 열 이름이 된다. (점으로 연결)

df = df.rename(columns={"items.water": "water", "items.ration": "ration"})
# 문법: .rename(columns={"옛이름": "새이름"}) = 열 이름 바꾸기. 지문이 요구한 이름과 똑같이.

df.to_csv("결과.csv", index=False)
print(df[["water", "ration"]].sum())
# 문법: df[[열1, 열2]].sum() = 열별 합계. 지문의 "항목별 총합 출력".
```

**④ 코드**

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
[↑ 목차](#목차)

**① 간단 개념 (세션 04)**

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

### 04-1. 부대별 통계 / 장비 사용 분포 / 설문 요약  
[↑ 세션 04](#세션-04-기술통계량)

**지문 요점**

1. 전체와 **부대(그룹)별** 평균·중앙값·표준편차
2. 평균·표준편차·최소·최대·중앙값, 최빈값
3. 결과를 csv로 저장(`health_stats.csv` 등)

**② 함수 정리 (PPT '활용 코드 정리')**

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

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 열 고르기 → 전체 통계 → 그룹별 통계 → 열 이름 정리 → 저장
cols = ["col_a", "col_b"]

overall = df[cols].agg(["mean", "median", "std"])
# 문법: .agg([통계 이름들]) = 여러 통계를 한 번에. 행 = 통계 이름, 열 = 원래 열. 결과는 표.

by_unit = df.groupby("unit")[cols].agg(["mean", "std"])
# 문법: df.groupby("그룹열") = 그룹으로 나눈다. [cols] = 그 안에서 볼 열. .agg(...) = 그룹마다 통계.
# 과정: 결과의 열 이름이 (col_a, mean)처럼 2단(MultiIndex)이 된다.

by_unit.columns = ["_".join(c) for c in by_unit.columns]
# 문법: "_".join(("col_a","mean")) = "col_a_mean". 2단 열 이름을 한 줄 이름으로 펼친다.

overall.to_csv("overall.csv"); by_unit.to_csv("by_unit.csv")
# 주의: 행 이름(mean/median, 부대명)이 인덱스에 있으므로 이 경우엔 index=False를 쓰지 않는다.
#   → 인덱스를 열로 내리려면 .reset_index().to_csv(..., index=False)

df[cols].mode().iloc[0]
# 문법: .mode() = 최빈값 표(동점이면 여러 행). .iloc[0] = 첫 번째 행만. (agg("mode")는 오류가 난다)

# ── 전체 + 그룹을 한 표로 합치기 ──
all_row = df[cols].agg(["mean", "std"]).T          # .T = 행·열 뒤집기
# 과정: 합치려면 모양이 같아야 한다. "행 = 대상, 열 = 통계"로 맞춘 뒤 pd.concat([전체, 그룹별])로 위아래 붙인다.
# 과정: concat(axis=0) 뒤에 reset_index()로 이름을 열로 내리고 저장.
```

**④ 코드**

```python
df = pd.read_csv("health_summary.csv")
cols = ["temperature", "pulse", "weight"]
overall = df[cols].agg(["mean", "median", "std"])
by_unit = df.groupby("unit")[cols].agg(["mean", "std"])
by_unit.columns = ["_".join(c) for c in by_unit.columns]
overall.to_csv("health_stats.csv"); by_unit.to_csv("unit_stats.csv")
df[cols].mode().iloc[0]
```


---

## 세션 05. 데이터 시각화  
[↑ 목차](#목차)

**① 간단 개념 (세션 05)**

- 도구: **matplotlib**, **seaborn**, plotly
- 차트: 막대(bar), 히스토그램, 박스플롯, 산점도, 파이 등
  - 히스토그램 = 분포 / 박스플롯 = 분포와 이상치 / 산점도 = 두 변수 관계
- **상관계수**(피어슨, `corr()`): −1~1. 부호는 방향, 절댓값이 클수록 관계가 강함. **heatmap**으로 한 번에 시각화.

### 05-1. 분포·이상치 / 산점도·상관 / 상관 heatmap  
[↑ 세션 05](#세션-05-데이터-시각화)

**지문 요점**

1. 히스토그램+박스플롯 → `plots/` 폴더에 저장
2. `training_pressure`–`command_tension` **산점도**
3. **상관계수 행렬 + heatmap**을 png로 저장

**② 함수 정리 (PPT '활용 코드 정리')**

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

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 폴더 만들기 → 여러 그래프를 한 그림에 그리기 → 저장 / 산점도 / 상관 heatmap
fig, ax = plt.subplots(2, 3, figsize=(14, 7))
# 문법: plt.subplots(행, 열) = 그림 한 장 안에 2×3 칸을 만든다. ax[행, 열]로 칸을 고른다.

for i, c in enumerate(cols):
    # 문법: enumerate(리스트) = (번호, 값)을 차례로. i = 0,1,2 → 칸의 열 번호, c = 열 이름.
    ax[0, i].hist(df[c], bins=15); ax[0, i].set_title(f"{c} hist")
    # 문법: .hist(값, bins=구간 수) = 히스토그램(분포). f"{c} hist" = 문자열 안에 변수 값 넣기.
    ax[1, i].boxplot(df[c]);       ax[1, i].set_title(f"{c} box")
    # 문법: .boxplot(값) = 박스플롯(중앙값·사분위·이상치 점).

os.makedirs("plots", exist_ok=True)
# 문법: os.makedirs(폴더, exist_ok=True) = 폴더 만들기. 이미 있어도 오류 없음. savefig 전에 필요.
plt.tight_layout(); plt.savefig("plots/dist.png"); plt.close()

sns.scatterplot(data=s, x="x열", y="y열", hue="그룹열")
# 문법: sns.scatterplot(data=표, x=, y=) = 산점도. hue = 그룹별 색 구분(선택).
plt.savefig("scatter.png"); plt.close()

sns.heatmap(s.select_dtypes("number").corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1)
# 문법: .select_dtypes("number") = 숫자 열만. .corr() = 열끼리 상관계수 표(−1~1).
# 문법: annot=True = 칸에 숫자 표시. vmin/vmax = 색 범위 고정. cmap = 색상표.
plt.tight_layout(); plt.savefig("corr.png"); plt.close()
```

**④ 코드**

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
[↑ 목차](#목차)

**① 간단 개념 (세션 06)**

- **상관관계로 해석**: 상관계수의 부호와 크기로 "어떤 관계인지" 문장으로 설명.
- **임계치(threshold)로 해석**: 기준값(중앙값 등)을 정해 높은 그룹/낮은 그룹으로 나눠 평균 비교.
- **groupby + mean**: 그룹별 평균. **idxmin/idxmax**: 가장 낮은/높은 항목 이름.
- **pivot_table** 4요소: ① 대상 DataFrame ② `index`(행) ③ `values`(값) ④ `aggfunc`(집계 방법)
- 지표 방향 주의: 수리 횟수처럼 **낮을수록 좋은** 지표가 있다.

### 06-1. 관계 해석 / 그룹 통계 / 운용 효율  
[↑ 세션 06](#세션-06-데이터-해석)

**지문 요점**

1. 두 변수의 **상관계수 + 해석**
2. **임계치**로 높은/낮은 그룹 평균 비교
3. `groupby` 평균, 가장 낮은 항목, `pivot_table`로 구조화

**② 함수 정리 (PPT '활용 코드 정리')**

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

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 상관계수 → 기준값으로 두 그룹 나누기 → 그룹 평균 비교 → groupby 평균 → 가장 낮은 항목 → pivot_table
r = df["col_a"].corr(df["col_b"])
# 문법: 열1.corr(열2) = 두 열의 상관계수(−1~1). 양수면 같이 증가, 음수면 반대로.
print(round(r, 3))
# 문법: round(값, 자리수) = 반올림.

th = df["col_x"].median()
# 과정: 기준값(임계치)을 정한다. 지문이 값을 주면 그것, 없으면 중앙값/평균.

hi = df[df["col_x"] > th]["col_y"].mean()
lo = df[df["col_x"] <= th]["col_y"].mean()
# 문법: df[조건] = 조건에 맞는 행만. 그 뒤 ["col_y"] = 그 행들의 열 → .mean() 평균.
# 과정: 높은 그룹과 낮은 그룹의 평균을 비교하고, 차이를 한 문장으로 해석한다.

avg = m.groupby("unit")[score].mean().round(2)
# 문법: groupby("그룹열")[열들].mean() = 그룹별 평균. .round(2) = 소수 둘째 자리까지.
avg.to_csv("avg.csv")

print(m[score].mean().idxmin())
# 문법: m[score].mean() = 열별 평균(Series). .idxmin() = 가장 작은 값의 이름. (idxmax는 가장 큰 값)
# 주의: 지표가 "낮을수록 좋은" 것인지(수리 횟수 등) 확인하고 해석.

pt = pd.pivot_table(m, index="unit", values=score, aggfunc="mean")
# 문법: pivot_table(표, index=행으로 쓸 열, values=값으로 쓸 열들, aggfunc=집계 방법) = 요약표.
# 과정: groupby().mean()과 결과가 비슷하다. 지문이 pivot_table이라고 하면 이걸 쓴다.
```

**④ 코드**

```python
df = pd.read_csv("stress_analysis.csv")
r = df["sleep_quality"].corr(df["training_pressure"]); print(round(r, 3))
th = df["command_tension"].median()
hi = df[df["command_tension"] > th]["sleep_quality"].mean()
lo = df[df["command_tension"] <= th]["sleep_quality"].mean()
print(round(hi, 2), round(lo, 2))

m = pd.read_csv("meal_feedback.csv"); score = ["taste_score", "quantity_score", "cleanliness_score"]
avg = m.groupby("unit")[score].mean().round(2); avg.to_csv("meal_unit_avg.csv")
print(m[score].mean().idxmin())
pt = pd.pivot_table(m, index="unit", values=score, aggfunc="mean")
```


---

## 세션 07. 지도학습 및 평가  
[↑ 목차](#목차)

**① 간단 개념 (세션 07)**

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

### 07-1. 전투 적합도 분류  
[↑ 세션 07](#세션-07-지도학습-및-평가)

**지문 요점**

1. `status`를 Label Encoding(적합=1, 부적합=0)
2. **8:2 분할** 후 RandomForestClassifier 학습
3. 예측 결과 csv 저장 + 정확도·혼동행렬·classification_report 출력

**② 함수 정리 (PPT '활용 코드 정리')**

- `train_test_split()` — 학습/테스트 분리  
  ↳ **언제**: 모델을 만들 때 항상 먼저. 평가는 **테스트셋**으로. 보통 `test_size=0.2, random_state=42`.
- `RandomForestClassifier / fit / predict` — 분류 모델 학습·예측  
  ↳ **언제**: 타깃이 범주. `fit`으로 학습 → `predict`로 예측.
- `accuracy_score / confusion_matrix / classification_report` — 분류 평가  
  ↳ **언제**: 분류 모델 평가. 지문에 적힌 지표를 모두 출력.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 정답 열 만들기 → X/y 나누기 → 학습/테스트 분할 → 학습 → 예측 → 결과 저장 → 평가 출력
df["y"] = (df["status"] == "적합").astype(int)
# 문법: (열 == 값) = 각 행이 같은지 True/False. .astype(int) = True/False → 1/0.
# 과정: 지문이 "적합=1, 부적합=0"이라고 했으니 이렇게 직접 지정. (LabelEncoder는 가나다 순이라 반대가 될 수 있다)

X = df[["col_a", "col_b"]]; y = df["y"]
# 과정: X = 문제를 푸는 데 쓰는 특징(여러 열, 대괄호 2개), y = 맞혀야 할 정답(열 하나). 정답 열은 X에서 뺀다.

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
# 문법: train_test_split(X, y, test_size=0.2) = 80% 학습 / 20% 테스트로 무작위 분할. 4개를 순서대로 돌려준다.
# 문법: random_state=42 = 같은 결과가 나오게 고정. 지문에 값이 있으면 그 값.

clf = RandomForestClassifier(random_state=42).fit(Xtr, ytr)
# 문법: 모델이름(옵션).fit(특징, 정답) = 학습. 학습 데이터만 넣는다.

pred = clf.predict(Xte)
# 문법: .predict(특징) = 예측값. 테스트 특징만 넣는다.

res = df.loc[Xte.index, ["soldier_id"]].copy()
# 문법: df.loc[행 이름들, 열들] = 이름으로 고르기. Xte.index = 테스트로 뽑힌 행 번호 → 그 행의 id만.
# 문법: .copy() = 복사본. (경고 방지)
res["actual"] = yte.values; res["pred"] = pred
# 문법: .values = 인덱스 없이 값만. 인덱스가 어긋나 NaN 되는 것을 막는다.
res.to_csv("결과.csv", index=False)

print(accuracy_score(yte, pred)); print(confusion_matrix(yte, pred)); print(classification_report(yte, pred))
# 문법: 평가함수(실제, 예측) 순서. 평가는 항상 "테스트 정답 vs 테스트 예측".
```

**④ 코드**

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
df = pd.read_csv("combat_ready.csv")
df["status_enc"] = (df["status"] == "적합").astype(int)
X = df[["pushup_count", "run_time_2km(sec)", "sprint_100m(sec)"]]; y = df["status_enc"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(random_state=42).fit(Xtr, ytr); pred = clf.predict(Xte)
res = df.loc[Xte.index, ["soldier_id"]].copy(); res["actual"] = yte.values; res["pred"] = pred
res.to_csv("combat_ready_result.csv", index=False)
print(accuracy_score(yte, pred)); print(confusion_matrix(yte, pred)); print(classification_report(yte, pred))
```

### 07-2. 장비 수명 예측(회귀)  
[↑ 세션 07](#세션-07-지도학습-및-평가)

**지문 요점**

1. **LinearRegression** 학습
2. 테스트 데이터 예측 + **RMSE**
3. `life_prediction.csv`(`equipment_id, predicted_life`) + 실제 vs 예측 그래프 저장

**② 함수 정리 (PPT '활용 코드 정리')**

- `LinearRegression` — 회귀 모델  
  ↳ **언제**: 타깃이 숫자이고 지문이 선형회귀를 지정했을 때.
- `mean_squared_error → RMSE` — 회귀 평가(RMSE = MSE의 제곱근)  
  ↳ **언제**: 회귀 평가. RMSE는 작을수록 좋음. 시험 환경에선 `np.sqrt(mean_squared_error)`.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: X/y 나누기 → 분할 → 선형회귀 학습 → 예측 → RMSE 계산 → 결과·그래프 저장
reg = LinearRegression().fit(Xtr, ytr)
# 문법: 분류와 같은 틀. 모델.fit(학습 특징, 학습 정답). 정답 y가 숫자일 때 회귀.
pred = reg.predict(Xte)

rmse = np.sqrt(mean_squared_error(yte, pred))
# 문법: mean_squared_error(실제, 예측) = MSE. np.sqrt(...) = 제곱근 → RMSE.
# 과정: 오래된 환경에서는 squared=False 옵션이 없을 수 있어 np.sqrt를 쓴다. 작을수록 좋다.
print(rmse, mean_absolute_error(yte, pred), r2_score(yte, pred))
# 문법: MAE(평균 절대오차, 작을수록 좋음), R²(1에 가까울수록 좋음).

pd.DataFrame({"equipment_id": df.loc[Xte.index, "equipment_id"], "predicted_life": pred}).to_csv("결과.csv", index=False)
# 문법: pd.DataFrame({열이름: 값들, ...}) = 사전으로 표 만들기. 지문이 정한 열 이름 그대로.

plt.scatter(yte, pred)
plt.plot([yte.min(), yte.max()], [yte.min(), yte.max()], "r--")
# 문법: plt.scatter(x, y) = 점. plt.plot([x1,x2],[y1,y2],"r--") = 빨간 점선 → 대각선(예측=실제).
# 과정: 점들이 대각선에 가까울수록 예측이 정확하다.
plt.xlabel("actual"); plt.ylabel("predicted"); plt.savefig("그래프.png"); plt.close()
```

**④ 코드**

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

### 07-3. 정비 시급성 다중분류  
[↑ 세션 07](#세션-07-지도학습-및-평가)

**지문 요점**

1. `priority_level`(A/B/C)을 Label Encoding
2. GradientBoosting 또는 RandomForest 다중 분류
3. classification_report·confusion_matrix + `priority_prediction.csv`

**② 함수 정리 (PPT '활용 코드 정리')**

- `GradientBoostingClassifier` — 다중분류 모델  
  ↳ **언제**: 3개 이상 클래스 분류. RandomForest와 같은 방식으로 `fit/predict`.

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 정답 글자 → 숫자 → 분할 → 학습 → 평가 → 예측값을 다시 글자로 → 저장
le = LabelEncoder(); y = le.fit_transform(df["priority_level"])
# 문법: 글자(A,B,C) 정답을 정수(0,1,2)로. 모델은 숫자 정답이 안전하다.

m = GradientBoostingClassifier(random_state=42).fit(Xtr, ytr); p = m.predict(Xte)
# 과정: RandomForest와 사용법이 똑같다(fit → predict). 3개 이상의 클래스도 그대로 된다.

print(classification_report(yte, p, target_names=le.classes_))
# 문법: target_names=le.classes_ = 0,1,2 대신 A,B,C 이름으로 표시.

out = df.loc[Xte.index, ["weapon_id"]].copy()
out["predicted"] = le.inverse_transform(p)
# 문법: le.inverse_transform(숫자) = 정수를 원래 글자(A,B,C)로 되돌린다. 저장 파일엔 글자로 쓰는 것이 보통.
out.to_csv("결과.csv", index=False)
```

**④ 코드**

```python
from sklearn.ensemble import GradientBoostingClassifier
df = pd.read_csv("maintenance_priority.csv")
le = LabelEncoder(); y = le.fit_transform(df["priority_level"])
X = df[["age_years", "error_logs_per_month", "functional_score", "last_repair_months"]]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m = GradientBoostingClassifier(random_state=42).fit(Xtr, ytr); p = m.predict(Xte)
print(classification_report(yte, p, target_names=le.classes_)); print(confusion_matrix(yte, p))
out = df.loc[Xte.index, ["weapon_id"]].copy(); out["predicted"] = le.inverse_transform(p)
out.to_csv("priority_prediction.csv", index=False)
```


---

## 세션 08. 비지도학습  
[↑ 목차](#목차)

**① 간단 개념 (세션 08)**

| 방법 | 설명 |
|---|---|
| 군집화 | 레이블 없는 데이터를 유사성에 따라 그룹(클러스터)으로 나눔. 데이터의 내재된 구조 파악, EDA에 유용 (`KMeans(n_clusters)`) |
| 차원 축소 | 고차원 데이터를 저차원으로 변환해 간소화, 중요한 패턴 유지 (`PCA`, `pca.components_`) |

**실루엣 계수**(군집이 잘 나뉘었는지): a(i) = 같은 군집 내 다른 점들과의 평균 거리, b(i) = 가장 가까운 다른 군집 점들과의 평균 거리. 일반식 s = (b − a) / max(a, b), −1~1이고 **클수록 좋음**.

### 08-1. 군집화 / PCA 2차원 / 근무 유형 군집  
[↑ 세션 08](#세션-08-비지도학습)

**지문 요점**

1. `KMeans(n_clusters=3)`, 결과 `cluster` 컬럼 저장
2. **StandardScaler → PCA 2차원** 후 산점도
3. `groupby('cluster').mean()`으로 군집 특성 해석

**② 함수 정리 (PPT '활용 코드 정리')**

- `KMeans(n_clusters=3)` — 군집화. 결과는 .labels_  
  ↳ **언제**: 정답 없이 N개 그룹으로 묶을 때. 군집 수는 지문이 정한다. 먼저 표준화.
- `PCA(n_components=2) / pca.components_` — 2차원 축소 / 축 구성 확인  
  ↳ **언제**: 열이 많을 때 2차원으로 줄여 시각화. `components_`로 각 축에 어떤 열이 크게 기여하는지 해석.
- `silhouette_score` — 군집 분리 정도(−1~1, 클수록 좋음)  
  ↳ **언제**: 군집이 잘 나뉘었는지 점수로 확인(1에 가까울수록 좋음).

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 열 고르기 → 표준화 → KMeans → 군집 번호 붙이기 → 해석 → PCA 2차원 → 그래프
feats = [c for c in df.columns if c != "soldier_id"]
# 문법: [c for c in 열들 if 조건] = 조건에 맞는 것만 모은 리스트. 여기선 id를 뺀 모든 열.

X = StandardScaler().fit_transform(df[feats])
# 과정: 거리로 묶는 알고리즘(KMeans, PCA)은 열마다 크기가 다르면 편향되므로 먼저 표준화.

km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
# 문법: KMeans(n_clusters=묶을 개수).fit(X) = 정답(y) 없이 X만 넣는다. 개수는 지문이 정한다.
df["cluster"] = km.labels_
# 문법: km.labels_ = 각 행이 속한 군집 번호(0,1,2).

print(silhouette_score(X, km.labels_))
# 문법: 실루엣 점수(−1~1, 클수록 군집이 잘 나뉨).

print(df.groupby("cluster")[feats].mean())
# 과정: 군집별 평균을 보고 "이 군집은 ~가 높은 유형"이라고 해석한다.
print(df["cluster"].value_counts().sort_index())
# 문법: .value_counts() = 값별 개수. .sort_index() = 군집 번호 순으로 정렬.

p = PCA(n_components=2).fit(X); Z = p.transform(X)
# 문법: PCA(n_components=2).fit(X) = 2개 축을 찾는다. .transform(X) = 각 행을 2차원 좌표(Z)로.
print(p.explained_variance_ratio_, p.components_)
# 문법: explained_variance_ratio_ = 각 축이 설명하는 비율. components_ = 각 축에 각 열이 기여하는 정도.

plt.scatter(Z[:, 0], Z[:, 1], c=df["cluster"], cmap="viridis")
# 문법: Z[:, 0] = 모든 행의 첫 번째 열(PC1), Z[:, 1] = PC2. c= 값에 따라 색을 칠한다.
plt.xlabel("PC1"); plt.ylabel("PC2"); plt.savefig("pca.png"); plt.close()
```

**④ 코드**

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
df = pd.read_csv("duty_pattern.csv"); feats = [c for c in df.columns if c != "soldier_id"]
X = StandardScaler().fit_transform(df[feats])
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X); df["cluster"] = km.labels_
print(silhouette_score(X, km.labels_)); print(df.groupby("cluster")[feats].mean())
print(df["cluster"].value_counts().sort_index())
p = PCA(n_components=2).fit(X); Z = p.transform(X); print(p.explained_variance_ratio_, p.components_)
plt.scatter(Z[:, 0], Z[:, 1], c=df["cluster"], cmap="viridis"); plt.xlabel("PC1"); plt.ylabel("PC2")
plt.savefig("duty_pca_plot.png"); plt.close(); df.to_csv("duty_clusters.csv", index=False)
```


---

## 세션 09. 이미지 처리 (OpenCV)  
[↑ 목차](#목차)

**① 간단 개념 (세션 09)**

- **OpenCV**: 컴퓨터 비전·머신러닝 오픈소스 라이브러리. 실시간 이미지 처리 중심(이미지·영상 처리, 객체 탐지 등).
- 학습 포인트: ① 이미지 읽고 처리 ② 윤곽선·도형 검출 ③ 객체 좌표 추출·데이터화
- 흐름: `imread`(BGR) → `cvtColor`(흑백) → `resize` → `GaussianBlur` → `Canny` → `findContours` → `approxPolyDP`/`arcLength`/`isContourConvex` → `boundingRect`
- **YOLO**: 사전학습 모델로 객체 탐지(클래스명, 좌표 x1·y1·x2·y2, 신뢰도).

### 09-1. 이미지 밝기  
[↑ 세션 09](#세션-09-이미지-처리-opencv)

**지문 요점**

1. 모든 이미지를 **256×256 리사이즈 → 흑백 → 평균 밝기**
2. `brightness_result.csv` 저장, 가장 밝은 파일명 출력

**② 함수 정리 (PPT '활용 코드 정리')**

- `cv2.imread(경로)` — 이미지 읽기(색 순서 BGR)
- `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` — 흑백 변환
- `cv2.resize(img, (256, 256))` — 크기 변경(가로, 세로)

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 폴더의 이미지를 하나씩 → 읽기 → 크기 통일 → 흑백 → 평균 밝기 기록 → 표로 저장
rows = []
# 문법: 빈 리스트. 결과를 한 줄씩 모아 두었다가 마지막에 표로 만든다.

for f in sorted(os.listdir("폴더")):
    # 문법: os.listdir(폴더) = 폴더 안 파일 이름 목록. sorted = 이름순 정렬(결과 순서 고정). for = 하나씩 반복.
    if not f.lower().endswith((".png", ".jpg", ".jpeg")): continue
    # 문법: .lower() = 소문자로. .endswith(튜플) = 그 확장자로 끝나는지. continue = 아니면 건너뛰기.
    img = cv2.imread(f"폴더/{f}")
    # 문법: cv2.imread(경로) = 이미지를 숫자 배열로. 색 순서는 BGR. f"..{f}" = 변수 값 넣은 문자열.
    img = cv2.resize(img, (256, 256))
    # 문법: cv2.resize(이미지, (가로, 세로)).
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 문법: cv2.cvtColor(이미지, 변환코드) = 색 변환. BGR→흑백.
    rows.append({"filename": f, "brightness": gray.mean()})
    # 문법: gray.mean() = 모든 픽셀 평균 = 평균 밝기(0~255). {...} = 한 줄 기록, append = 리스트에 추가.

b = pd.DataFrame(rows); b.to_csv("결과.csv", index=False)
# 문법: 딕셔너리 리스트 → 표. 키가 열 이름이 된다.
print(b.loc[b["brightness"].idxmax(), "filename"])
# 문법: .idxmax() = 가장 큰 값의 행 번호 → .loc[행, "열"]로 그 행의 파일명.
```

**④ 코드**

```python
import cv2
rows = []
for f in sorted(os.listdir("images/night_ops")):
    if not f.lower().endswith((".png", ".jpg", ".jpeg")): continue
    img = cv2.imread(f"images/night_ops/{f}")
    img = cv2.resize(img, (256, 256))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows.append({"filename": f, "brightness": gray.mean()})
b = pd.DataFrame(rows); b.to_csv("brightness_result.csv", index=False)
print(b.loc[b["brightness"].idxmax(), "filename"])
```

### 09-2. 설계도 사각형 검출  
[↑ 세션 09](#세션-09-이미지-처리-opencv)

**지문 요점**

1. `findContours`로 윤곽 검출
2. `approxPolyDP`로 **사각형만** 필터링
3. 이미지별 (x,y,width,height)와 사각형 수를 `rectangles.csv`에 저장

**② 함수 정리 (PPT '활용 코드 정리')**

- `cv2.GaussianBlur(img, (5,5), 0)` — 흐리게(잡음 제거)
- `cv2.Canny(img, 50, 150)` — 윤곽선(엣지) 검출
- `cv2.findContours(...)` — 윤곽 찾기
- `cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)` — 윤곽을 꼭짓점 N개 도형으로 단순화
- `cv2.isContourConvex(ap)` — 볼록 도형인지
- `cv2.boundingRect(ap)` — 외접 사각형 (x, y, w, h)

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 이미지마다 → 흑백 → 흐리게 → 윤곽선 → 윤곽 찾기 → 꼭짓점 4개인 것만 → 좌표 기록
edges = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 50, 150)
# 문법: GaussianBlur(이미지, (5,5), 0) = 잡음 제거용 흐리게. Canny(이미지, 낮은기준, 높은기준) = 윤곽선(엣지)만 남기기.

cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 문법: findContours = 윤곽 목록(cnts)을 찾는다. 반환이 2개라 `_`는 안 쓰는 값. RETR_EXTERNAL = 가장 바깥 윤곽만.

n = 0
for c in cnts:
    # 문법: 윤곽 하나씩 반복.
    ap = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
    # 문법: arcLength(윤곽, True) = 둘레 길이. approxPolyDP(윤곽, 허용오차, 닫힌도형) = 꼭짓점이 적은 도형으로 단순화.
    # 과정: 허용오차를 둘레의 2%로. 사각형이면 꼭짓점 4개로 단순화된다.
    if len(ap) == 4 and cv2.isContourConvex(ap):
        # 문법: len(ap) = 꼭짓점 수. isContourConvex = 오목하지 않은 도형인지. 둘 다 만족해야 사각형.
        x, y, w, h = cv2.boundingRect(ap); n += 1
        # 문법: boundingRect = 도형을 감싸는 사각형의 (왼쪽 위 x, y, 가로, 세로). n += 1 = 개수 세기.
        rows.append({"filename": f, "x": x, "y": y, "width": w, "height": h})
pd.DataFrame(rows).to_csv("rectangles.csv", index=False)
```

**④ 코드**

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

### 09-3. 객체 탐지(YOLO)와 좌표 저장  
[↑ 세션 09](#세션-09-이미지-처리-opencv)

**지문 요점**

1. 사전학습 **YOLOv5**로 사람·차량 탐지
2. 클래스명과 (x1,y1,x2,y2) 추출
3. `detections.csv`(`filename, class, x1, y1, x2, y2`), 사람/차량 수 출력

**② 함수 정리 (PPT '활용 코드 정리')**

- `PIL.Image.open(경로)` — 이미지 열기
- `torch.hub.load('ultralytics/yolov5','yolov5s', pretrained=True)` — YOLOv5 모델 불러오기
- `results.pandas().xyxy[0]` — 탐지 결과 표(`xmin ymin xmax ymax confidence class name`)

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: YOLO 모델 불러오기 → 이미지마다 탐지 → 결과 표의 행을 한 줄씩 기록 → 저장 → 개수 세기
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
# 문법: torch.hub.load(저장소, 모델이름) = 사전학습 YOLO 불러오기. 처음엔 인터넷이 필요.

img = cv2.imread(경로)[:, :, ::-1]
# 문법: [:, :, ::-1] = 색 채널 순서를 뒤집는다(BGR → RGB). 모델은 RGB를 기대.

d = model(img).pandas().xyxy[0]
# 문법: model(이미지) = 탐지 실행. .pandas().xyxy[0] = 결과를 표로(xmin,ymin,xmax,ymax,confidence,class,name).

for _, r in d.iterrows():
    # 문법: .iterrows() = 표를 한 행씩. (행 번호, 행) 중 번호는 안 쓰므로 `_`.
    rows.append({"filename": f, "class": r["name"], "x1": r.xmin, "y1": r.ymin, "x2": r.xmax, "y2": r.ymax})
    # 과정: 지문이 정한 열 이름(x1,y1,x2,y2)으로 바꿔 담는다.

det = pd.DataFrame(rows); det.to_csv("detections.csv", index=False)
print((det["class"] == "person").sum(), det["class"].isin(["car", "truck", "bus"]).sum())
# 문법: (열 == 값).sum() = 개수. .isin([여러 값]) = 목록에 있는 것이면 True.
```

**④ 코드**

```python
import torch
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
rows = []
for f in sorted(os.listdir("images/surv_imgs")):
    img = cv2.imread(f"images/surv_imgs/{f}")[:, :, ::-1]
    d = model(img).pandas().xyxy[0]
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

**클래스 이름 바꾸기·합치기 (후처리)** — 사전학습 모델에 없는 클래스(예: 탱크)를 다루라는 문제를 대비한 패턴

> **언제 쓰나**: 사전학습 YOLO(COCO 80개 클래스)에는 탱크 같은 군 장비 클래스가 없습니다. 비슷하게 탐지된 클래스(`truck`, `car` 등)를 문제 지시대로 **다른 이름으로 바꾸거나 합쳐서** 집계할 때 쓴다. 정확히 학습시키라는 지시면 아래 파인튜닝을 쓴다.

```python
# det: filename, class, x1, y1, x2, y2 (위에서 만든 탐지 결과 표)
class_map = {"truck": "tank", "car": "tank"}      # {탐지된 이름: 부를 이름} — 문제 지시대로
det["class"] = det["class"].replace(class_map)
det = det[det["class"].isin(["person", "tank"])]  # 필요한 클래스만 남기기
print(det["class"].value_counts())
```

```python
# ultralytics(YOLOv8): 사전학습 클래스 목록 확인 → 새 클래스로 파인튜닝 (CPU: 작은 모델·작은 이미지·적은 epoch)
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
print(model.names)                      # {0: 'person', 2: 'car', 7: 'truck', ...} — 'tank' 없음 확인
# 새 클래스를 쓰려면 data.yaml(train/val 경로, names: [새 클래스 목록])을 준비한 뒤
# model.train(data="data.yaml", epochs=10, imgsz=416, batch=8, device="cpu")
```



---

## 세션 10. 이미지 분류·OCR·영상  
[↑ 목차](#목차)

**① 간단 개념 (세션 10)**

- 탐지 결과를 **통계화**(클래스별 빈도) → `Counter`, 상위 N개 막대그래프
- **OCR**: 이미지 속 글자 인식(`easyocr.Reader`, `readtext`), 정규식 `re`로 한글·영문·숫자만 추출
- **영상**: `cv2.VideoCapture` → `isOpened()` → `read()`로 프레임 추출(예: 30FPS면 30프레임마다 1초 간격)
- 이미지에서 추출한 정보를 표로 만들어 csv로 저장

### 10-1. 객체 빈도 통계  
[↑ 세션 10](#세션-10-이미지-분류ocr영상)

**지문 요점**

1. 각 이미지에 YOLO 탐지
2. 클래스별 **전체 빈도**를 `object_count.csv`에
3. **상위 3개** 막대그래프 `top3_objects.png`

**② 함수 정리 (PPT '활용 코드 정리')**

- `[f for f in os.listdir(d) if f.lower().endswith(('.jpg','.png','.jpeg'))]` — 폴더에서 이미지 파일만 모으기
- `collections.Counter(리스트)` / `.most_common(3)` — 빈도 세기 / 상위 3개

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 클래스 이름 목록 → 빈도 세기 → 표로 정렬해 저장 → 상위 3개 막대그래프
cnt = Counter(det["class"])
# 문법: Counter(목록) = 값별 개수를 센 사전 형태. (from collections import Counter)

pd.DataFrame(cnt.items(), columns=["class", "count"]).sort_values("count", ascending=False).to_csv("object_count.csv", index=False)
# 문법: cnt.items() = (이름, 개수) 쌍들. columns=로 열 이름 지정. sort_values(열, ascending=False) = 내림차순.

top3 = cnt.most_common(3)
# 문법: .most_common(N) = 개수가 많은 순서로 (이름, 개수) 상위 N개 리스트.

plt.bar([k for k, _ in top3], [v for _, v in top3])
# 문법: plt.bar(이름들, 값들) = 막대그래프. 컴프리헨션으로 이름 목록(k)과 개수 목록(v)을 따로 뽑는다.
plt.title("Top3 objects"); plt.savefig("top3_objects.png"); plt.close()
```

**④ 코드**

```python
from collections import Counter
cnt = Counter(det["class"])
pd.DataFrame(cnt.items(), columns=["class", "count"]).sort_values("count", ascending=False).to_csv("object_count.csv", index=False)
top3 = cnt.most_common(3)
plt.bar([k for k, _ in top3], [v for _, v in top3]); plt.title("Top3 objects"); plt.savefig("top3_objects.png"); plt.close()
```

### 10-2. 이미지 속 글자(OCR)  
[↑ 세션 10](#세션-10-이미지-분류ocr영상)

**지문 요점**

1. `easyocr`로 텍스트 추출
2. **정규식**으로 한글·영문·숫자만 남김
3. `supply_info.csv` 저장

**② 함수 정리 (PPT '활용 코드 정리')**

- `easyocr.Reader(['ko','en'])` / `readtext(경로)` — 글자 인식 모델 / 인식 실행 → (좌표, 글자, 신뢰도)
- `re.match(r'^[가-힣A-Za-z0-9]+$', text)` — 정규식으로 한글·영문·숫자만 통과

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: OCR 모델 만들기 → 이미지마다 글자 읽기 → 조건에 맞는 글자만 → 표로 저장
reader = easyocr.Reader(["ko", "en"], gpu=False)
# 문법: easyocr.Reader(언어 목록, gpu=False) = 한글+영어 인식 모델. 첫 실행 때 모델을 내려받아 오래 걸린다.

for bbox, text, conf in reader.readtext(경로):
    # 문법: .readtext(이미지경로) = [(글자 위치, 글자, 신뢰도), ...]. for에서 3개를 한 번에 풀어 받는다.
    if re.match(r"^[가-힣A-Za-z0-9\s]+$", text):
        # 문법: re.match(패턴, 글자) = 패턴에 맞으면 결과, 아니면 None(False).
        # 문법: ^ 시작, $ 끝, [가-힣A-Za-z0-9\s] = 한글·영문·숫자·공백 중 하나, + = 1개 이상.
        # 과정: 처음부터 끝까지 전부 허용 글자로만 이루어진 것만 통과(특수문자가 섞이면 제외).
        rows.append({"filename": f, "text": text, "conf": round(conf, 3)})
pd.DataFrame(rows).to_csv("supply_info.csv", index=False)
```

**④ 코드**

```python
import easyocr, re
reader = easyocr.Reader(["ko", "en"], gpu=False)
rows = []
for f in sorted(os.listdir("images/supplies_imgs")):
    for bbox, text, conf in reader.readtext(f"images/supplies_imgs/{f}"):
        if re.match(r"^[가-힣A-Za-z0-9\s]+$", text):
            rows.append({"filename": f, "text": text, "conf": round(conf, 3)})
pd.DataFrame(rows).to_csv("supply_info.csv", index=False)
```

### 10-3. 드론 영상 프레임 탐지  
[↑ 세션 10](#세션-10-이미지-분류ocr영상)

**지문 요점**

1. **1초 간격**으로 프레임 추출(30FPS → 30프레임마다)
2. 각 프레임 YOLO 탐지
3. `drone_detection.csv`(`frame_number, class, x1, y1, x2, y2`) + 프레임별 개수 시계열 그래프

**② 함수 정리 (PPT '활용 코드 정리')**

- `cv2.VideoCapture(경로)` / `isOpened()` / `read()` — 영상 열기 / 열렸는지 / 프레임 한 장 읽기(`ok, frame`)
- `cap.get(cv2.CAP_PROP_FPS)` — 초당 프레임 수

**③ 코드 설명 (줄마다 문법·과정)**

```python
# 과정: 영상 열기 → 초당 프레임 수 → 한 프레임씩 읽기 → 1초마다 하나만 저장
cap = cv2.VideoCapture("영상.mp4")
# 문법: VideoCapture(경로) = 영상을 열어 프레임을 읽을 수 있게 한다.
assert cap.isOpened(), "영상을 열 수 없음"
# 문법: assert 조건, 메시지 = 조건이 거짓이면 오류로 멈춘다. isOpened() = 잘 열렸는지.

fps = int(round(cap.get(cv2.CAP_PROP_FPS))) or 30
# 문법: cap.get(CAP_PROP_FPS) = 초당 프레임 수. round → int로 정수. `or 30` = 0이면 30으로.

i, frames = 0, []
# 문법: i는 프레임 번호, frames는 저장할 프레임 목록.
while True:
    # 문법: while True = 멈추라고 할 때까지 반복.
    ok, frame = cap.read()
    # 문법: .read() = 다음 프레임 한 장. ok = 읽기 성공 여부, frame = 이미지.
    if not ok: break
    # 과정: 영상이 끝나면 ok가 False → 반복 종료.
    if i % fps == 0: frames.append((i, frame))
    # 문법: i % fps = 나머지. 0이면 fps 프레임마다 한 번 = 1초 간격. (번호, 이미지) 쌍으로 저장.
    i += 1
cap.release()
# 문법: 영상 닫기. 이후 frames의 각 이미지에 YOLO를 적용해 결과를 저장한다.
```

**④ 코드**

```python
cap = cv2.VideoCapture("videos/drone_mission.mp4")
assert cap.isOpened(), "영상을 열 수 없음"
fps = int(round(cap.get(cv2.CAP_PROP_FPS))) or 30
i, frames = 0, []
while True:
    ok, frame = cap.read()
    if not ok: break
    if i % fps == 0: frames.append((i, frame))
    i += 1
cap.release(); print(len(frames), "프레임 추출")
```


---

## 한글·인코딩 (깨짐 방지)  
[↑ 목차](#목차)

CSV를 읽고 저장할 때 한글이 깨지는 문제를 막는 규칙입니다. (아래 동작은 실제로 3가지 인코딩으로 저장해 pandas와 파이썬 `csv`로 읽어서 확인했습니다.)

**읽을 때 — 깨지거나 `UnicodeDecodeError`가 나면**

```python
def read_csv_auto(path, **kw):
    for enc in ("utf-8", "utf-8-sig", "cp949", "ISO-8859-1"):   # 앞에서부터 시도
        try:
            return pd.read_csv(path, encoding=enc, **kw)
        except UnicodeDecodeError:
            continue
    raise ValueError("인코딩 판별 실패")
```
- **초기 코드에 `encoding="ISO-8859-1"`처럼 지정돼 있으면 그대로 따른다**(사전 테스트의 미세먼지 데이터가 그랬음).
- 한글 윈도우 엑셀에서 저장한 csv는 보통 `cp949`.

**저장할 때 — 기본은 그냥 utf-8**

| 저장 방식 | pandas로 읽기 | 파이썬 `csv`/`open`으로 읽기 | 언제 쓰나 |
|---|---|---|---|
| `df.to_csv("x.csv", index=False)` (utf-8) | 한글 정상 | 한글 정상 | **제출 파일 기본값(가장 안전)** |
| `df.to_csv("x.csv", index=False, encoding="utf-8-sig")` | 한글 정상 | 첫 열 이름이 `\ufeff예보 등급`처럼 앞에 BOM이 붙음 | 엑셀에서 열었을 때 한글이 깨질 때, 또는 **제공된 sample 파일이 BOM 형식일 때** |
| `encoding="cp949"` | 기본 읽기에서 오류 | 오류 | 지문이 요구할 때만 |

- **sample 파일이 있으면 그 형식을 따른다**: `open("sample.csv", "rb").read(3) == b"\xef\xbb\xbf"`가 `True`이면 BOM(utf-8-sig) 파일.
- `utf-8-sig`는 pandas가 BOM을 자동으로 지워서 안전하지만, pandas가 아닌 방식으로 읽으면 첫 열 이름이 달라질 수 있어서 **필요할 때만** 씁니다.
- **저장 직후 다시 읽어서 확인**: `pd.read_csv("x.csv").head()` — 열 이름과 한글 값이 그대로인지 봅니다.

**그래프의 한글**
- 서버에 한글 폰트가 없으면 제목·축 이름이 □로 깨집니다. **제목과 축 이름은 영어로** 쓰는 것이 안전합니다.
- 마이너스 부호가 깨지면 `plt.rcParams["axes.unicode_minus"] = False`.
- 한글 폰트가 필요하면(있을 때만): `plt.rcParams["font.family"] = "NanumGothic"` (윈도우는 `"Malgun Gothic"`). 폰트 확인: `from matplotlib import font_manager as fm; [f.name for f in fm.fontManager.ttflist if "Nanum" in f.name or "Malgun" in f.name]`


---

## 종합문제 대비 (세션 11·12)  
[↑ 목차](#목차)

종합문제는 세션 01~10의 조합입니다: 표 데이터 회귀·분류(세션 07), 이상 탐지(IsolationForest)·PCA(세션 08), 이미지 인원·차량 수(세션 09·10 YOLO), 결과 csv·그래프 저장.

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

## 공통 시작 코드  
[↑ 목차](#목차)

> **언제 쓰나**: 모든 문제의 시작. 파일을 읽을 땐 `read_csv`, 결과 저장은 반드시 `to_csv(index=False)`. 한글 깨지면 `encoding='cp949'`.

```python
import os, numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
df = pd.read_csv("data.csv")            # 한글 깨지면 encoding="cp949"
df.head(); df.info(); df.describe(); df.isna().sum(); df.shape
df.to_csv("result.csv", index=False)    # index=False 필수
os.makedirs("plots", exist_ok=True)
```