"""Тесты для GitHub Actions"""
import pytest

def test_math():
    assert 2 + 2 == 4

def test_string():
    assert "hello".upper() == "HELLO"

def test_list():
    assert sum([1, 2, 3]) == 6
