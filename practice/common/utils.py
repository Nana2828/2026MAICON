"""예선 연습용 공통 유틸. 시험장 노트북에 셀로 그대로 붙여넣어 쓸 수 있게 의존성을 최소화했다."""
import os
import random
import time
from contextlib import contextmanager

import numpy as np
import pandas as pd

SEED = 42


def seed_everything(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except ImportError:
        pass


@contextmanager
def timer(name: str = ""):
    t = time.time()
    yield
    print(f"[{name}] {time.time() - t:.1f}s")


def read_csv_auto(path: str, **kw) -> pd.DataFrame:
    """인코딩을 자동으로 시도한다(utf-8 → cp949 → latin-1). KAMP/공공데이터는 cp949가 흔하다."""
    for enc in ("utf-8", "utf-8-sig", "cp949", "ISO-8859-1"):
        try:
            return pd.read_csv(path, encoding=enc, low_memory=False, **kw)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"인코딩을 판별하지 못했습니다: {path}")


def quick_eda(df: pd.DataFrame, target: str | None = None) -> None:
    print("shape:", df.shape)
    print(df.dtypes.value_counts().to_string(), "\n")
    na = df.isna().mean().sort_values(ascending=False)
    print("결측 비율 상위:\n", na[na > 0].head(10).to_string() or "없음", "\n")
    if target and target in df:
        print("타깃 분포:\n", df[target].value_counts(normalize=True).head(10).to_string())


def save_submission(df: pd.DataFrame, path: str, expected_cols=None, expected_rows=None) -> None:
    """제출 csv 저장 + 형식 검증. 시험의 '데이터 검증' 전에 로컬에서 먼저 확인한다."""
    if expected_cols is not None:
        assert list(df.columns) == list(expected_cols), f"컬럼 불일치: {list(df.columns)} != {list(expected_cols)}"
    if expected_rows is not None:
        assert len(df) == expected_rows, f"행 수 불일치: {len(df)} != {expected_rows}"
    assert not df.isna().any().any(), "제출 파일에 결측이 있습니다"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    df.to_csv(path, index=False)
    print(f"저장 완료: {path} {df.shape}")
