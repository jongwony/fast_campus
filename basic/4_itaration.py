from typing import Iterable, Sequence, Iterator

# List는 Sequence이자 Iterable입니다.
sequence = [1, 2, 3]

# List로부터 Iterator 생성
iterator = iter(sequence)

# Generator는 Iterator이자 Iterable입니다.
def my_generator():
    yield 1
    yield 2
    yield 3

generator = my_generator()

# 타입 확인
print(isinstance(sequence, Iterable))  # True
print(isinstance(sequence, Sequence))  # True
print(isinstance(sequence, Iterator))  # False

print(isinstance(iterator, Iterable))  # True
print(isinstance(iterator, Sequence))  # False
print(isinstance(iterator, Iterator))  # True

print(isinstance(generator, Iterable))  # True
print(isinstance(generator, Sequence))  # False
print(isinstance(generator, Iterator))  # True