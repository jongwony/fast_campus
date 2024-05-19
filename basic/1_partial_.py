from functools import partial


# 기본적인 연산자를 다루는 함수
def add(a, b):
    return a + b

# add 함수의 첫 번째 인수를 5로 고정한 add_five 함수 생성
add_five = partial(add, 5)

# 새로운 함수 사용
print(add_five(10))  # 출력: 15 (5 + 10)
print(add_five(3))   # 출력: 8  (5 + 3)


# 문자열을 다루면서 사용하는 함수
def format_greeting(greeting, name):
    return f"{greeting}, {name}!"

# greeting을 "Hello"로 고정한 format_hello 함수 생성
format_hello = partial(format_greeting, "Hello")

# 새로운 함수 사용
print(format_hello("Alice"))  # 출력: Hello, Alice!
print(format_hello("Bob"))    # 출력: Hello, Bob!


# 데이터 처리 함수에서 사용하는 함수
def transform_data(data, multiplier, offset):
    return [(x * multiplier) + offset for x in data]

# multiplier를 2로 고정하고 offset을 3으로 고정한 transform_example 함수 생성
transform_example = partial(transform_data, multiplier=2, offset=3)

# 새로운 함수 사용
data = [1, 2, 3, 4]
print(transform_example(data))  # 출력: [5, 7, 9, 11]
