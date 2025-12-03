from src.library import Library, PrintedBook


def test_add_book():
    lib = Library()
    book = PrintedBook("Test Book", "Author", 2020, 100, "хорошая")
    lib.add_book(book)
    assert lib.find_book("Test Book") == book
