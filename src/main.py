def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


def multiply(a: int, b: int) -> int:  # 👈 НОВАЯ ФУНКЦИЯ
    return a * b


if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))
