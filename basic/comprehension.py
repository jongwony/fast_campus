"""
아래의 코드는 모두 같은 결과를 출력합니다
"""
# Comprehension
squares = [x**2 for x in [1, 2, 3, 4, 5]]


# Map
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))


# Map with function
def square(x):
    return x**2


squares = list(map(square, numbers))


# For loop
squares = []
for i in [1, 2, 3, 4, 5]:
    squares.append(i**2)


##############################################

# Comprehension
even = [x for x in [1, 2, 3, 4, 5] if x % 2 == 0]


# Filter
numbers = [1, 2, 3, 4, 5]
even = list(filter(lambda x: x % 2 == 0, numbers))


# Filter with function
def is_even(x):
    return x % 2 == 0


even = list(filter(is_even, numbers))


# For loop
even = []
for i in [1, 2, 3, 4, 5]:
    if i % 2 == 0:
        even.append(i)


##############################################

# Comprehension
pairs = [(x, y) for x in [1, 2, 3] for y in [4, 5, 6]]

# For loop
pairs = []
for x in [1, 2, 3]:
    for y in [4, 5, 6]:
        pairs.append((x, y))
