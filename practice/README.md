# 2026 국방 AI 경진대회 예선 연습

예선 형식: Jupyter(Python3), 3문항 / 90분, 결과 csv 제출, GPU 없음, 검색·AI 보조 도구 사용 가능
(단, 문제 지문·제공 데이터를 외부 AI에 그대로 입력해 정답을 생성하는 것은 금지).

## 구성
| 파일 | 내용 |
|---|---|
| `notebooks/00_jupyter_basics.ipynb` | Jupyter 입문, 단축키, 시험 당일 루틴 |
| `notebooks/01_tabular_modeling.ipynb` | 표 데이터 전처리·CV·베이스라인 제출 |
| `notebooks/02_timeseries_sensor.ipynb` | 센서/시계열 윈도우 특징, 시간순 검증 |
| `notebooks/03_image_transfer_yolo.ipynb` | CPU 전이학습(ResNet18 임베딩), YOLO 사용법 |
| `notebooks/04_text_classification.ipynb` | TF-IDF 텍스트 분류 |
| `common/utils.py` | 인코딩 자동판별 csv 로드, 제출 파일 검증 등 |

## 데이터 (저장소에 올리지 않음)
`practice/data/`에 **직접** 내려받아 넣으세요. `.gitignore`가 데이터와 csv 커밋을 막습니다.
- 공식 교육자료: maicon.kr 예선 안내의 `DST_Training_Materials.zip` (교안·실습파일)
- KAMP 공개 데이터셋: kamp-ai.kr 에서 로그인 후 다운로드
- 대회 본 데이터·문제·사전 테스트 체험 데이터는 **절대 올리지 마세요** (공유 금지 규정).

데이터 파일이 없으면 노트북은 합성 데모 데이터로 흐름만 실행됩니다.
각 노트북 첫 CONFIG 셀의 파일명·타깃 컬럼만 바꿔 쓰세요.

## 설치
```
pip install -r practice/requirements.txt
# 이미지/YOLO 연습 시: pip install torch torchvision ultralytics
```
