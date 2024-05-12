from functools import reduce

# 두 숫자를 더하는 함수
def add(x, y):
    return x + y

numbers = [1, 2, 3, 4, 5]

# reduce 함수를 사용하여 numbers 리스트의 모든 숫자를 더함
result = reduce(add, numbers)

print(result)  # 출력: 15

##############################################

scores = [88, 92, 79, 93, 85]
weights = [0.2, 0.2, 0.25, 0.15, 0.2]
weighted_scores = [score * weight for score, weight in zip(scores, weights)]
final_score = sum(weighted_scores)
print(f"Weighted final score: {final_score:.2f}")


# 같은 결과를 reduce 함수를 사용하여 구현
scores = [88, 92, 79, 93, 85]
weights = [0.2, 0.2, 0.25, 0.15, 0.2]
weighted_scores = map(lambda x, y: x * y, scores, weights)
final_score = reduce(lambda x, y: x + y, weighted_scores)
print(f"Weighted final score: {final_score:.2f}")
# 출력: Weighted final score: 86.70


##############################################

# 여러 거래에서의 순 이익을 계산할 때 각 단계별로 특정 조건에 따라 세금을 공제하거나 보너스를 추가하는 복잡한 누적 로직을 적용해야 할 때 reduce를 사용할 수 있습니다.
# 이는 reduce가 단순히 값을 더하는 것을 넘어서, 각 단계에서의 복잡한 조건부 논리를 적용할 수 있음을 보여줍니다.
# 이 코드는 각 거래를 처리하면서, 거래가 양수인 경우 세금으로 10%를 공제하고, 음수인 경우 (예: 비용) 그대로 누적합니다. 이처럼 reduce는 복잡한 조건과 누적 계산을 한 번에 처리할 수 있는 유연성을 제공합니다.
transactions = [100, 200, -50, 300, -100]
net_income = reduce(lambda acc, x: (acc + x) * 0.9 if x > 0 else acc + x, transactions, 0)
print(f"Net income after taxes and deductions: {net_income:.2f}")
