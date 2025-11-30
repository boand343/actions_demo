import unittest
from src.library import Book, PrintedBook, EBook, Library


class TestLibrary(unittest.TestCase):
    def test_book_init(self):
        b = Book("Война и мир", "Толстой", 1869)
        self.assertEqual(b.title, "Война и мир")
        self.assertEqual(b.author, "Толстой")
        self.assertEqual(b.year, 1869)

    def test_printed_book_inherits_book(self):
        b = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
        self.assertIsInstance(b, Book)

    def test_ebook_inherits_book(self):
        b = EBook("451° по Фаренгейту", "Брэдбери", 1953, "pdf")
        self.assertIsInstance(b, Book)

    def test_library_create(self):
        lib = Library()
        self.assertIsNotNone(lib)


if name == "__main__":
    unittest.main()