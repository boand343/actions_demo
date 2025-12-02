'''import unittest
from src.main import add, subtract


class TestMathFunctions(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 2), 3)
        self.assertEqual(subtract(0, 3), -3)


if __name__ == "__main__":
    unittest.main()'''

import unittest
import sys
import io
from contextlib import redirect_stdout
from src.main import Book, PrintedBook, EBook, User, Librarian, Library


class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book("Test Title", "Test Author", 2020)
        self.assertEqual(book.get_title(), "Test Title")
        self.assertEqual(book.get_author(), "Test Author")
        self.assertEqual(book.get_year(), 2020)
        self.assertTrue(book.is_available())

    def test_book_mark_as_taken(self):
        book = Book("Test Title", "Test Author", 2020)
        book.mark_as_taken()
        self.assertFalse(book.is_available())

    def test_book_mark_as_returned(self):
        book = Book("Test Title", "Test Author", 2020)
        book.mark_as_taken()
        book.mark_as_returned()
        self.assertTrue(book.is_available())

    def test_book_str(self):
        book = Book("Test Title", "Test Author", 2020)
        book_str = str(book)
        self.assertIn("Test Title", book_str)
        self.assertIn("Test Author", book_str)
        self.assertIn("2020", book_str)


class TestPrintedBook(unittest.TestCase):
    def test_printed_book_creation(self):
        pbook = PrintedBook("Test Title", "Test Author", 2020, 300, "хорошая")
        self.assertEqual(pbook.get_title(), "Test Title")
        self.assertEqual(pbook._pages, 300)
        self.assertEqual(pbook._condition, "хорошая")

    def test_repair_from_bad_to_good(self):
        pbook = PrintedBook("Test Title", "Test Author", 2020, 300, "плохая")
        result = pbook.repair()
        self.assertEqual(pbook._condition, "хорошая")
        self.assertEqual(result, "сделали из плохой, хорошую")

    def test_repair_already_good(self):
        pbook = PrintedBook("Test Title", "Test Author", 2020, 300, "хорошая")
        result = pbook.repair()
        self.assertEqual(result, "Книга уже в хорошем состоянии")

    def test_repair_new(self):
        pbook = PrintedBook("Test Title", "Test Author", 2020, 300, "новая")
        result = pbook.repair()
        self.assertEqual(result, "Книга новая")


class TestEBook(unittest.TestCase):
    def test_ebook_creation(self):
        ebook = EBook("Test Title", "Test Author", 2020, 10, "pdf")
        self.assertEqual(ebook.get_title(), "Test Title")
        self.assertEqual(ebook._file_size, 10)
        self.assertEqual(ebook._format, "pdf")

    def test_ebook_download(self):
        ebook = EBook("Test Title", "Test Author", 2020, 10, "pdf")
        f = io.StringIO()
        with redirect_stdout(f):
            ebook.download()
        output = f.getvalue()
        self.assertIn("Test Title", output)
        self.assertIn("10", output)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("Test User")
        self.book = Book("Test Book", "Test Author", 2020)

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.get_borrowed_books(), [])

    def test_borrow_book(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.user.borrow(self.book)
        output = f.getvalue()
        self.assertIn("Test User", output)
        self.assertIn("Test Book", output)
        self.assertFalse(self.book.is_available())
        self.assertIn(self.book, self.user.get_borrowed_books())

    def test_borrow_unavailable_book(self):
        self.book.mark_as_taken()
        f = io.StringIO()
        with redirect_stdout(f):
            self.user.borrow(self.book)
        output = f.getvalue()
        self.assertIn("недоступна", output)

    def test_return_book(self):
        self.user.borrow(self.book)
        f = io.StringIO()
        with redirect_stdout(f):
            self.user.return_book(self.book)
        output = f.getvalue()
        self.assertIn("вернул", output)
        self.assertTrue(self.book.is_available())
        self.assertNotIn(self.book, self.user.get_borrowed_books())

    def test_return_book_not_borrowed(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.user.return_book(self.book)
        output = f.getvalue()
        self.assertIn("нет книги", output)


class TestLibrarian(unittest.TestCase):
    def setUp(self):
        self.librarian = Librarian("Test Librarian")
        self.library = Library()
        self.book = Book("Test Book", "Test Author", 2020)
        self.user = User("Test User")

    def test_librarian_creation(self):
        self.assertEqual(self.librarian.name, "Test Librarian")
        self.assertIsInstance(self.librarian, User)

    def test_add_book(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.librarian.add_book(self.library, self.book)
        output = f.getvalue()
        self.assertIn("добавлена", output)

    def test_register_user(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.librarian.register_user(self.library, self.user)
        output = f.getvalue()
        self.assertIn("добавлен", output)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book1 = Book("Book 1", "Author 1", 2000)
        self.book2 = Book("Book 2", "Author 2", 2001)
        self.user = User("Test User")

    def test_add_book(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.library.add_book(self.book1)
        output = f.getvalue()
        self.assertIn("добавлена", output)

    def test_find_book(self):
        self.library.add_book(self.book1)
        found = self.library.find_book("Book 1")
        self.assertEqual(found, self.book1)

    def test_find_nonexistent_book(self):
        found = self.library.find_book("Nonexistent")
        self.assertIsNone(found)

    def test_add_user(self):
        f = io.StringIO()
        with redirect_stdout(f):
            self.library.add_user(self.user)
        output = f.getvalue()
        self.assertIn("добавлен", output)

    def test_lend_book(self):
        self.library.add_book(self.book1)
        self.library.add_user(self.user)
        f = io.StringIO()
        with redirect_stdout(f):
            self.library.lend_book("Book 1", "Test User")
        output = f.getvalue()
        self.assertIn("взял книгу", output)


if __name__ == "__main__":
    unittest.main()
