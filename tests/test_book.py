from src.taskClass import Book


def test_book_creation():
    book = Book("Title", "Author", 2000, available=True)
    assert book.get_title() == "Title"
    assert book.get_author() == "Author"
    assert book.get_year() == 2000
    assert book.get_available() is True


def test_mark_taken_and_return():
    book = Book("T", "A", 2000, available=True)
    book.mark_as_taken()
    assert book.get_available() is False
    book.mark_as_returned()
    assert book.get_available() is True
