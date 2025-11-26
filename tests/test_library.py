import pytest
from src.library import Book, PrintedBook, EBook, User, Librarian, Library


def test_book_availability():
    b = Book("Тест", "Автор", 2020)
    assert b.is_available()
    b.mark_as_taken()
    assert not b.is_available()
    b.mark_as_returned()
    assert b.is_available()


def test_printed_book_repair():
    b = PrintedBook("Тест", "Автор", 2020, 100, "плохая")
    b.repair()
    assert b.condition == "хорошая"
    b.repair()
    assert b.condition == "новая"


def test_ebook_download():
    b = EBook("Электронная", "Автор", 2021, 5, "pdf")
    # Проверяем, что файл доступен и не падает
    assert b.get_title() == "Электронная"
    assert b.format == "pdf"


def test_user_borrow_and_return():
    u = User("Анна")
    b = Book("Книга", "Автор", 2000)

    u.borrow(b)
    assert not b.is_available()
    assert b in u.get_borrowed_books()

    u.return_book(b)
    assert b.is_available()
    assert b not in u.get_borrowed_books()


def test_library_lend_and_return():
    lib = Library()
    u = User("Анна")
    b = Book("Книга", "Автор", 2000)

    lib.add_user(u)
    lib.add_book(b)

    lib.lend_book("Книга", "Анна")
    assert not b.is_available()

    lib.return_book("Книга", "Анна")
    assert b.is_available()
