import pytest
from src.main import add, subtract


class TestMathFunctions:
    """Тесты для математических функций"""
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел"""
        assert add(2, 3) == 5
        assert add(0, 0) == 0
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел"""
        assert add(-2, -3) == -5
        assert add(-2, 3) == 1
    
    def test_subtract_positive_numbers(self):
        """Тест вычитания положительных чисел"""
        assert subtract(5, 3) == 2
        assert subtract(3, 5) == -2
    
    def test_subtract_negative_numbers(self):
        """Тест вычитания отрицательных чисел"""
        assert subtract(-5, -3) == -2
        assert subtract(-5, 3) == -8
    
    def test_add_large_numbers(self):
        """Тест сложения больших чисел"""
        assert add(1000000, 2000000) == 3000000
    
    def test_subtract_large_numbers(self):
        """Тест вычитания больших чисел"""
        assert subtract(5000000, 3000000) == 2000000
