import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.library import Book, PrintedBook, EBook, User, Librarian, Library


class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("1984", "George Orwell", 1949)

    def test_book_creation(self):
        self.assertEqual(self.book.get_title(), "1984")
        self.assertEqual(self.book.get_author(), "George Orwell")
        self.assertEqual(self.book.get_year(), 1949)

    def test_book_available_by_default(self):
        self.assertTrue(self.book.is_available())

    def test_mark_as_taken(self):
        self.book.mark_as_taken()
        self.assertFalse(self.book.is_available())

    def test_mark_as_returned(self):
        self.book.mark_as_taken()
        self.book.mark_as_returned()
        self.assertTrue(self.book.is_available())


class TestPrintedBook(unittest.TestCase):
    def setUp(self):
        self.book = PrintedBook("War and Peace", "Leo Tolstoy", 1869, 1200, "хорошая")

    def test_printed_book_creation(self):
        self.assertEqual(self.book.pages, 1200)
        self.assertEqual(self.book.condition, "хорошая")

    def test_repair_from_bad_to_good(self):
        book = PrintedBook("Test", "Author", 2000, 300, "плохая")
        book.repair()
        self.assertEqual(book.condition, "хорошая")

    def test_repair_from_good_to_new(self):
        book = PrintedBook("Test", "Author", 2000, 300, "хорошая")
        book.repair()
        self.assertEqual(book.condition, "новая")


class TestEBook(unittest.TestCase):
    def setUp(self):
        self.ebook = EBook("Digital Book", "Author Name", 2020, 50, "PDF")

    def test_ebook_creation(self):
        self.assertEqual(self.ebook.file_size, 50)
        self.assertEqual(self.ebook.format, "PDF")

    def test_ebook_inheritance(self):
        self.assertTrue(self.ebook.is_available())


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("Alice")
        self.book = Book("Test Book", "Test Author", 2020)

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Alice")

    def test_borrow_book(self):
        self.user.borrow(self.book)
        self.assertEqual(len(self.user.get_borrowed_books()), 1)
        self.assertFalse(self.book.is_available())

    def test_return_book(self):
        self.user.borrow(self.book)
        self.user.return_book(self.book)
        self.assertEqual(len(self.user.get_borrowed_books()), 0)
        self.assertTrue(self.book.is_available())

    def test_cannot_borrow_unavailable_book(self):
        self.book.mark_as_taken()
        initial_count = len(self.user.get_borrowed_books())
        self.user.borrow(self.book)
        self.assertEqual(len(self.user.get_borrowed_books()), initial_count)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book1 = Book("Book 1", "Author 1", 2020)
        self.book2 = Book("Book 2", "Author 2", 2021)
        self.user = User("Bob")

    def test_add_book(self):
        self.library.add_book(self.book1)
        found_book = self.library.find_book("Book 1")
        self.assertIsNotNone(found_book)

    def test_find_book(self):
        self.library.add_book(self.book1)
        found = self.library.find_book("Book 1")
        self.assertEqual(found.get_title(), "Book 1")

    def test_find_nonexistent_book(self):
        found = self.library.find_book("Nonexistent")
        self.assertIsNone(found)

    def test_add_user(self):
        self.library.add_user(self.user)
        found_user = self.library.find_user("Bob")
        self.assertIsNotNone(found_user)

    def test_lend_book(self):
        self.library.add_book(self.book1)
        self.library.add_user(self.user)
        self.library.lend_book("Book 1", "Bob")
        self.assertFalse(self.book1.is_available())

    def test_return_book(self):
        self.library.add_book(self.book1)
        self.library.add_user(self.user)
        self.library.lend_book("Book 1", "Bob")
        self.library.return_book("Book 1", "Bob")
        self.assertTrue(self.book1.is_available())


class TestLibrarian(unittest.TestCase):
    def setUp(self):
        self.librarian = Librarian("John")
        self.library = Library()
        self.book = Book("New Book", "Author", 2022)

    def test_librarian_add_book(self):
        self.librarian.add_book(self.library, self.book)
        found = self.library.find_book("New Book")
        self.assertIsNotNone(found)

    def test_librarian_remove_book(self):
        self.library.add_book(self.book)
        self.librarian.remove_book(self.library, "New Book")
        found = self.library.find_book("New Book")
        self.assertIsNone(found)


if __name__ == '__main__':
    unittest.main()