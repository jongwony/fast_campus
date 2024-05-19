class Person:
    def __init__(self, name, age):
        """
        생성자: constructor
        """
        # 속성: 상태를 저장하는 데이터
        self.name = name
        self.age = age
    
    def greet(self):
        """
        메서드: 기능 데이터를 조작하는 함수
        """
        return f"Hello, my name is {self.name}."

class BankAccount:
    """
    상태 관리 예제 balance 를 시도때도 없이 조회하고 싶을 때
    """
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds")
    
    def get_balance(self):
        return self.balance


account = BankAccount(100)
print(account.get_balance())  # Output: 100
account.deposit(50)
print(account.get_balance())  # Output: 150
account.withdraw(30)
print(account.get_balance())  # Output: 120
account.withdraw(200)  # Output: Insufficient funds
print(account.get_balance())  # Output: 120



def serialize_instance(obj):
    """
    dict -> JSON 직렬화
    """
    d = {'__classname__': type(obj).__name__}
    d.update(vars(obj))
    return d


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Dictionary mapping names to known classes
classes = {
    'Point': Point
}

def unserialize_object(d):
    """
    JSON -> dict 역직렬화
    """
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        return cls(**d)
    else:
        return d


# 직렬화 예제
p = Point(2, 3)
json_data = serialize_instance(p)
print(json_data)  # 출력: {'__classname__': 'Point', 'x': 2, 'y': 3}

# 역직렬화 예제
json_data = {'__classname__': 'Point', 'x': 2, 'y': 3}
p = unserialize_object(json_data)
print(p.x, p.y)  # 출력: 2 3
