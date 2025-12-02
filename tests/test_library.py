import os
import sys
from src.taskClass import Library, Book, User


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_library_add_and_find_book():
    lib = Library()
    b = Book("Title", "Author", 2000, available=True)
    lib.add_book(b)
    assert lib.find_book("Title") == b


def test_library_add_user_and_find():
    lib = Library()
    u = User("Анна")
    lib.add_user(u)
    assert lib.find_user("Анна") == u


def test_lend_and_return():
    lib = Library()
    u = User("Анна")
    b = Book("Title", "A", 2000, available=True)
    lib.add_user(u)
    lib.add_book(b)
    assert lib.lend_book("Title", "Анна") is True
    assert b.get_available() is False
    assert lib.return_book("Title", "Анна") is True
    assert b.get_available() is True
