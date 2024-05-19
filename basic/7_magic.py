class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __call__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


v1 = Vector(2, 3)
v2 = Vector(4, 5)
print(v1)  # Vector(2, 3)
print(repr(v1))  # Vector(2, 3)
v3 = v1 + v2
print(v3)  # Vector(6, 8)
print(len(v1))  # 2
print(v1[0], v1[1])  # 2 3
print(v1 == v2)  # False
print(v1())  # 3.605551275463989