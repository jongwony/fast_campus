from collections import defaultdict

# 기본 defaultdict 설정
fruits = defaultdict(list)

# 딕셔너리에 값 추가
fruits["사과"].append(1)
fruits["사과"].append(2)
fruits["바나나"].append(3)

print(fruits)
# 출력: {'사과': [1, 2], '바나나': [3]}

# 기본 딕셔너리를 사용하면 새로운 키에 접근할 때 KeyError가 발생하지만, defaultdict를 사용하면 이 문제를 피할 수 있습니다.
# d_fruits = {}
# d_fruits["사과"].append(1)

# zip 함수는 두 개 이상의 시퀀스를 짝지어서 튜플의 리스트로 만들어줍니다.
a = [1, 2, 3]
b = ['a', 'b', 'c']
zipped = zip(a, b)
print(list(zipped))
# 출력: [(1, 'a'), (2, 'b'), (3, 'c')]

# zip 함수를 사용하면 여러 시퀀스를 동시에 순회할 수 있습니다.
scores = {
    "Alice": 88,
    "Bob": 95,
    "Charlie": 70,
    "David": 100,
    "Eve": 65
}

# zip 함수를 사용하여 딕셔너리의 키와 값을 뒤집은 튜플을 만듭니다.
min_key = min(zip(scores.values(), scores.keys()))[1]
print(f"최소값을 가진 사람: {min_key}")
# 출력: 최소값을 가진 사람: Eve

max_key = max(zip(scores.values(), scores.keys()))[1]
print(f"최대값을 가진 사람: {max_key}")
# 출력: 최대값을 가진 사람: David

sorted_scores = sorted(zip(scores.values(), scores.keys()))
print("값으로 정렬된 리스트:")
for value, key in sorted_scores:
    print(f"{key}: {value}")
# 출력:
# 값으로 정렬된 리스트:
# Eve: 65
# Charlie: 70
# Alice: 88
# Bob: 95
# David: 100

sorted_keys = sorted(scores.items())
print("키로 정렬된 리스트:")
for key, value in sorted_keys:
    print(f"{key}: {value}")
# 출력:
# 키로 정렬된 리스트:
# Alice: 88
# Bob: 95
# Charlie: 70
# David: 100
# Eve: 65


# 각 항목에 키 파라미터를 적용한 예시: 키를 사용하여 추출한 값으로 계산(그림 설명 필요)
min_key = min(scores, key=scores.get)
print(f"최소값을 가진 사람: {min_key} ({scores[min_key]})")
# 출력: 최소값을 가진 사람: Eve (65)

max_key = max(scores, key=scores.get)
print(f"최대값을 가진 사람: {max_key} ({scores[max_key]})")
# 출력: 최대값을 가진 사람: David (100)

sorted_scores = sorted(scores.items(), key=lambda item: item[1])
print("값으로 정렬된 리스트:")
for key, value in sorted_scores:
    print(f"{key}: {value}")
# 출력:
# 값으로 정렬된 리스트:
# Eve: 65
# Charlie: 70
# Alice: 88
# Bob: 95
# David: 100

sorted_keys = sorted(scores.items(), key=lambda item: item[0])
print("키로 정렬된 리스트:")
for key, value in sorted_keys:
    print(f"{key}: {value}")
# 출력:
# 키로 정렬된 리스트:
# Alice: 88
# Bob: 95
# Charlie: 70
# David: 100
# Eve: 65

rows = [
    {'fname': '종원', 'lname': '최', 'uid': 1003},
    {'fname': '민수', 'lname': '김', 'uid': 1001},
    {'fname': '영희', 'lname': '박', 'uid': 1002},
    {'fname': '철수', 'lname': '이', 'uid': 1005},
    {'fname': '지훈', 'lname': '최', 'uid': 1004}
]

from operator import itemgetter

# 'lname'과 'fname'을 기준으로 정렬
sorted_rows = sorted(rows, key=itemgetter('lname', 'fname'))
sorted_rows_lambda = sorted(rows, key=lambda x: (x['lname'], x['fname']))

print("정렬된 리스트:")
for row in sorted_rows:
    print(row)

"""
temgetter와 lambda의 차이점
가독성:

itemgetter는 가독성이 높습니다. 특히 단일 키로 정렬할 때 코드가 간결하고 읽기 쉽습니다.
lambda는 다소 복잡할 수 있지만, 익숙한 사람들에게는 매우 유연합니다.
성능:

itemgetter는 C로 구현되어 있어, 다중 키 정렬의 경우 일반적으로 lambda보다 조금 더 빠릅니다.
lambda는 파이썬 레벨에서 동작하므로, 복잡한 키 조합이 필요한 경우 약간 느릴 수 있습니다.
유연성:

lambda는 더 유연합니다. 복잡한 키 조합이나 계산이 필요한 경우 유리합니다.
itemgetter는 단순한 키 접근만 지원하지만, 그만큼 사용하기 쉽습니다.
"""


# 집합 연산이 가능한 dict
scores1 = {
    "Alice": 88,
    "Bob": 95,
    "Charlie": 70
}

scores2 = {
    "Charlie": 70,
    "David": 100,
    "Eve": 65
}

# 딕셔너리의 키를 집합으로 변환
keys1 = set(scores1.keys())
keys2 = set(scores2.keys())

# 교집합 (공통된 키)
common_keys = keys1 & keys2
print(f"교집합 (공통된 키): {common_keys}")
# 출력: 교집합 (공통된 키): {'Charlie'}

# 합집합 (모든 키)
all_keys = keys1 | keys2
print(f"합집합 (모든 키): {all_keys}")
# 출력: 합집합 (모든 키): {'Charlie', 'Alice', 'David', 'Eve', 'Bob'}

# 차집합 (첫 번째 딕셔너리에만 있는 키)
unique_keys1 = keys1 - keys2
print(f"차집합 (첫 번째 딕셔너리에만 있는 키): {unique_keys1}")
# 출력: 차집합 (첫 번째 딕셔너리에만 있는 키): {'Alice', 'Bob'}


# 딕셔너리의 항목을 집합으로 변환
items1 = set(scores1.items())
items2 = set(scores2.items())

# 교집합 (공통된 항목)
common_items = items1 & items2
print(f"교집합 (공통된 항목): {common_items}")
# 출력: 교집합 (공통된 항목): {('Charlie', 70)}

# 합집합 (모든 항목)
all_items = items1 | items2
print(f"합집합 (모든 항목): {all_items}")
# 출력: 합집합 (모든 항목): {('Bob', 95), ('Eve', 65), ('Charlie', 70), ('Alice', 88), ('David', 100)}

# 차집합 (첫 번째 딕셔너리에만 있는 항목)
unique_items1 = items1 - items2
print(f"차집합 (첫 번째 딕셔너리에만 있는 항목): {unique_items1}")
# 출력: 차집합 (첫 번째 딕셔너리에만 있는 항목): {('Alice', 88), ('Bob', 95)}


scores1 = {
    "Alice": 88,
    "Bob": 95,
    "Charlie": 70
}

scores2 = {
    "Charlie": 70,
    "David": 100,
    "Eve": 65
}

# 딕셔너리의 키를 집합으로 변환
keys1 = set(scores1.keys())
keys2 = set(scores2.keys())

# 교집합 (공통된 키)
common_keys = keys1 & keys2
print(f"교집합 (공통된 키): {common_keys}")
# 출력: 교집합 (공통된 키): {'Charlie'}

# 합집합 (모든 키)
all_keys = keys1 | keys2
print(f"합집합 (모든 키): {all_keys}")
# 출력: 합집합 (모든 키): {'Charlie', 'Alice', 'David', 'Eve', 'Bob'}

# 차집합 (첫 번째 딕셔너리에만 있는 키)
unique_keys1 = keys1 - keys2
print(f"차집합 (첫 번째 딕셔너리에만 있는 키): {unique_keys1}")
# 출력: 차집합 (첫 번째 딕셔너리에만 있는 키): {'Alice', 'Bob'}


# 딕셔너리의 항목을 집합으로 변환
items1 = set(scores1.items())
items2 = set(scores2.items())

# 교집합 (공통된 항목)
common_items = items1 & items2
print(f"교집합 (공통된 항목): {common_items}")
# 출력: 교집합 (공통된 항목): {('Charlie', 70)}

# 합집합 (모든 항목)
all_items = items1 | items2
print(f"합집합 (모든 항목): {all_items}")
# 출력: 합집합 (모든 항목): {('Bob', 95), ('Eve', 65), ('Charlie', 70), ('Alice', 88), ('David', 100)}

# 차집합 (첫 번째 딕셔너리에만 있는 항목)
unique_items1 = items1 - items2
print(f"차집합 (첫 번째 딕셔너리에만 있는 항목): {unique_items1}")
# 출력: 차집합 (첫 번째 딕셔너리에만 있는 항목): {('Alice', 88), ('Bob', 95)}


# 합쳐서 값을 덮어쓰는 연산은 dict 로도 됩니다. 하지만 교집합, 차집합은 안됩니다.
# 아래 두 연산은 같습니다
print(scores1 | scores2) # python 3.9부터 가능
print(dict(scores1, **scores2))
# TypeError: unsupported operand type(s) for &: 'dict' and 'dict'
# print(scores1 & scores2)
# print(scores1 - scores2)
