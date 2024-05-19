import pandas as pd
import numpy as np
from functools import partial


data = {
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': [100, 200, 300, 400, 500]
}
df = pd.DataFrame(data)
print(df)


def log_transform(x, base):
    return np.log(x) / np.log(base)

# 로그 변환 함수의 base를 10으로 고정
log_transform_base_10 = partial(log_transform, base=10)


# 컬럼 'A'와 'B'에 로그 변환 함수 적용
df['A_log10'] = df['A'].apply(log_transform_base_10)
df['B_log10'] = df['B'].apply(log_transform_base_10)

print(df)
