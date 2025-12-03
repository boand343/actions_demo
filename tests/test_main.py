import sys
import os

# Добавляем папку src в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import add, subtract


def test_add_positive():
    """Тест сложения положительных чисел"""
    assert add(2, 3) == 5


def test_add_negative():
    """Тест сложения отрицательных чисел"""
    assert add(-2, -3) == -5


def test_add_mixed():
    """Тест сложения положительного и отрицательного"""
    assert add(5, -3) == 2


def test_subtract_positive():
    """Тест вычитания положительных чисел"""
    assert subtract(5, 3) == 2


def test_subtract_negative():
    """Тест вычитания отрицательных чисел"""
    assert subtract(-5, -3) == -2


def test_subtract_mixed():
    """Тест вычитания положительного и отрицательного"""
    assert subtract(5, -3) == 8
