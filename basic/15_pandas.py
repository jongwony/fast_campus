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
df['A_log10'] = df['A'].map(log_transform_base_10)
df['B_log10'] = df['B'].apply(log_transform_base_10)

print(df)



def test(x):
    breakpoint()
    return x['C'] + x['D']


df = pd.DataFrame(
    {'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar'],
     'B': ['one', 'one', 'two', 'three', 'two', 'two'],
     'C': [1, 5, 5, 2, 5, 5],
     'D': [2.0, 5., 8., 1., 2., 9.]}
)



df['E'] = df.apply(lambda x: x['C'] + x['D'], axis=1)
df.transform(lambda x: x['C'] + x['D'], axis=1)
df.apply(test, axis=0)
df.transform(test, axis=0)

df.groupby('A').apply(test)
df.groupby('A')[['C', 'D']].apply(test)
df.groupby('A').transform(test)
df.groupby('A')[['C', 'D']].transform(test)

df1 = pd.DataFrame({'key': ['A', 'B', 'C'], 'value': [1, 2, 3]})
df2 = pd.DataFrame({'key': ['A', 'B', 'D'], 'value': [4, 5, 6]})

merged_df = pd.merge(df1, df2, on='key', how='inner')