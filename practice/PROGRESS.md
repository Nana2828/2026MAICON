# 진행 메모 (이어서 공부할 때 이 파일부터 읽기)

> 마지막 갱신: 2026-10-10(시험 당일). 시험: **2026-10-10(토)** 14:00~, 90분, 3문항(20/35/45점), Jupyter·Python3.
> 시험 문제·데이터·작년 문항 같은 **시험 관련 정보는 이 저장소에 넣지 않는다.**

## 1. 공부 진행 상황
| 세션 | 주제 | 상태 |
|---|---|---|
| 01 | 결측치·이상치 | 완료 |
| 02 | 정규화·인코딩 | 완료 (모의 문제 풀이) |
| 03 | 시계열·JSON | 완료 |
| 04 | 기술통계량 (agg, groupby, mode, concat/reset_index) | 완료 (문제 1~3) |
| 05 | 시각화 (hist/boxplot, scatterplot, 상관 heatmap) | 완료 (혼자 풀이, 한 셀 규칙·`ax=`·`rotation=0` 확인) |
| 06 | 데이터 해석 (corr 해석, 임계치 비교, groupby, idxmin, pivot_table) | 완료 |
| 07 | 지도학습 (분류·회귀·다중분류, 분할 시 id 함께, 평가 해석, 저장, 선 그래프) | 완료 |
| 08 | 비지도학습 (표준화, KMeans `fit_predict`, PCA `fit_transform`, `components_` 해석, 군집 산점도) | 완료 |
| 09 | 이미지 (리사이즈·흑백·밝기, 사각형 검출, YOLOv5 탐지) | 완료 |
| 10 | 이미지·OCR·영상 (Counter 빈도, easyocr, 영상 1초 프레임 + YOLO + 프레임별 개수 그래프) | 풀이 진행 (문제 1·3 거의 완료, 2 OCR 진행) |
| 11~12 | 종합문제 | `practice/mock_exam/`에 90분 모의고사로 준비됨 (풀지 않음) |

**아직 안 한 것**: 텍스트 분류(`practice/notebooks/04_text_classification` 보강 필요), 모의고사 11·12.

## 2. 파일 위치
- GitHub: `Nana2828/2026MAICON`, 브랜치 **`claude/maicon-prelim-practice`** (PR #1은 main에 병합됨, 이후 수정은 같은 브랜치에 계속 올림)
- **`practice/cheatsheet/CHEATSHEET.md`** : 통합 치트시트. 세션마다 **① 간단 개념 → 지문 요점 → ② 함수 정리 → ③ 코드 설명(줄마다 `# 문법`·`# 과정` 주석) → 바꿔야 하는 부분 표(코드 속 → 내 문제에서는) → ④ 코드(복붙용)** 구조 + 하이퍼링크(목차·지문 키워드·함수 빠른 찾기), 시험 당일 체크리스트, 한글·인코딩. 시험 중에는 GitHub 웹에서 열어 둔다.
- 내 컴퓨터 위치: `C:\\study\\2026MAICON\\practice\\cheatsheet\\CHEATSHEET.md` (최신본을 받아 덮어쓰기 하거나 `git pull origin claude/maicon-prelim-practice`)
- 옛 분리본: `practice/cheatsheet/archive/`
- 연습 노트북 `practice/notebooks/`, 모의고사 `practice/mock_exam/`
- 공식 교육자료(수업 PDF·실습 zip)는 저장소에 없음 → 내 컴퓨터 `C:\study\공식실습`, 풀이는 `C:\study\my_work`

## 3. 환경
- **집 컴퓨터(Windows)**: Python 설치 관리자로 최신 안정 버전 설치, 명령은 `py`. Jupyter는 폴더 주소창에 `cmd` → `py -m notebook`.
  - **스마트 앱 컨트롤** 때문에 `scipy`·`sklearn`이 import 차단됨 → pandas·matplotlib까지만 로컬에서, **모델·scipy는 Google Colab**에서 한다.
  - 시험 서버는 별개라 이 문제와 무관. 시험 환경은 Python 3.9 + pandas 1.x로 보임 (`np.sqrt(mean_squared_error)`, `resample("H")` 사용).
- 집 컴퓨터에 `opencv-python`, `torch`, `ultralytics`, `easyocr`를 `py -m pip install`로 설치해 이미지·YOLO·OCR 연습 가능 (설치 중 `cv2.pyd` 접근 거부가 나면 노트북을 완전히 끄고 명령 프롬프트에서 설치). 실습 이미지는 노트북과 같은 폴더(`./night_ops/` 등)에 두면 `./images/…` 대신 `./폴더/…` 경로를 쓴다.
- **Colab**: colab.research.google.com → 파일 → 새 노트북 → 왼쪽 폴더 아이콘으로 csv 업로드(세션이 끝나면 사라짐, 다시 업로드). 그래프 한글은 깨지므로 제목·축은 영어. 한글이 꼭 필요하면 `!sudo apt-get install -y fonts-nanum` + 세션 다시 시작 + `plt.rcParams['font.family']='NanumGothic'`.
- 푼 노트북(`.ipynb`)은 GitHub에 자동으로 안 올라가므로 컴퓨터를 옮길 땐 OneDrive/USB 등으로 `my_work`를 옮긴다.

## 4. 공부 방식 (Claude에게 요청하는 방식)
- **시험처럼**: 내가 일반화한 질문(열 이름은 `col`처럼)을 하면 필요한 것만 답한다. 다음 단계는 묻기 전에 알려 주지 않는다.
- 코드 안내는 **예시 코드 + 줄마다 `# 문법`·`# 과정` 주석** 형식, 아래에 **"바꿔야 하는 부분(코드 속 → 내 문제에서는)" 표**.
- 힌트는 가능하면 **공식 교안(ipynb) 표현**(예: `kmeans.fit_predict`, `pca.fit_transform`, `Counter.update`, `results.pandas().xyxy[0]`)으로.
- 시각화는 **한 셀**에서 `figure → 그리기 → 제목·축(영어) → savefig → show → close` 순서.
- 데이터 분할은 **id 열도 함께 나누는 형식**: `Xtr, Xte, ytr, yte, ids_train, ids_test = train_test_split(X, y, df["id"], ...)`.
- 폴더의 이미지 목록: `img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]` 형식으로 안내.
- 치트시트에 추가할 주의점은 말하면 해당 세션에 반영 (단, "자주 나는 실수" 모음은 필요 없다고 함).

## 5. 시험 중 AI 사용 규칙 (사용자가 사무국에 확인한 내용 + 가이드)
- AI 보조 도구 사용은 가능, 결과 책임은 본인 (가이드 p.23).
- **문제 지문의 전체·일부를 복사·캡처하는 것은 금지**(시험 규정 p.16) → 지문은 AI에 넣지 않고, 필요한 작업만 **일반화해서** 질문.
- 데이터의 `head/info/describe/type` 정보를 알려 주는 것은 **사용자가 사무국에 확인했다고 전달한 내용**이다(저장소 기준으로는 미검증). 확인 답변(메일/캡처)은 따로 보관할 것.
- 노트북 안에서 문제·셀을 자동으로 읽는 AI 플러그인은 쓰지 않는다. 받은 코드는 직접 타이핑해서 내 문제에 맞게 바꾼다.
- 제공 데이터의 다운로드·외부 저장, 클라우드 자동 업로드(OneDrive 등), 화면 공유, 다중 접속은 금지 예시이므로 시험 데이터는 시험 서버에서만 작업.

## 6. 시험 당일 핵심 (자세한 것은 치트시트 "시험 당일 체크리스트")
- 입실 13:00, 응시 14:00부터, **16:30 일괄 종료 → 늦어도 15:00 전에 시작**
- 문항 순서 무관, 쉬운 것부터 베이스라인 csv 저장 → '데이터 검증' → 시간 남으면 개선
- **초기화 버튼 금지**, 시험 중 `.ipynb` 자주 저장, 마지막에 **최종 제출 및 테스트 종료**(1회)
- 사전 테스트 체험 결과 제출(10/1 마감)을 했는지 확인할 것. 안 했다면 사무국(02-6736-7419, contact@maicon.kr) 문의.

## 7. 알아 둘 점
- 치트시트는 `archive/`의 옛 분리본과 빌드 스크립트로 만들었다. 내용 수정은 `CHEATSHEET.md`를 직접 고치면 된다.
- 교육 영상은 선택, 시험 출제 범위(이미지·YOLO·텍스트 분류·모델 성능 개선)와 영상 내용이 다를 수 있다.
