from functools import reduce

# 데이터와 윈도우 크기
data = [10, 20, 30, 40, 50, 60, 70, 80]
window_size = 3

# 윈도우 연산을 위한 함수 정의
def rolling_window_average(acc, new):
    window, average = acc
    window.append(new)
    if len(window) > window_size:
        window.pop(0)
    new_average = sum(window) / len(window)
    print(window, new_average)
    breakpoint()
    return (window, new_average)

# 초기 윈도우와 평균
initial = ([], 0)

# 윈도우 평균 계산
_, averages = reduce(rolling_window_average, data, initial)
print(f"Rolling window averages: {averages}")