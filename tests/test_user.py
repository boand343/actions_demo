from src.taskClass import User, Book


def test_user_borrow_and_return():
    user = User("Анна")
    book = Book("Title", "Author", 2000, available=True)
    assert user.borrow(book) is True
    assert book.get_available() is False
    assert len(user.get_borrowed_books()) == 1
    assert user.return_book(book) is True
    assert book.get_available() is True
    assert len(user.get_borrowed_books()) == 0
