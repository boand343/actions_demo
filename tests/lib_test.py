import unittest
from src.Fedotov_12_11 import (
    Book,
    PrintedBook,
    EBook,
    User,
    Librarian,
    Library
)


class TestLibrarySystem(unittest.TestCase):

    def test_book_basic(self):
        book = Book("Тест", "Автор", 2000)
        self.assertEqual(book.get_title(), "Тест")
        self.assertEqual(book.get_author(), "Автор")
        self.assertEqual(book.get_year(), 2000)
        self.assertTrue(book.is_available())

        book.mark_as_taken()
        self.assertFalse(book.is_available())

        book.mark_as_returned()
        self.assertTrue(book.is_available())

    def test_printed_book_repair(self):
        book = PrintedBook("Название", "Автор", 2020, 300, "плохая")
        book.repair()
        self.assertEqual(book.condition, "хорошая")

        book.repair()
        self.assertEqual(book.condition, "новая")

    def test_ebook_download(self):
        ebook = EBook("Электронная", "Автор", 2021, 5, "epub")
        # Проверяем, что метод существует и не вызывает ошибок
        ebook.download()  # если упадёт — unittest засчитает ошибку

    def test_user_borrow_return(self):
        user = User("Анна")
        book = Book("Книга", "Автор", 2000)

        user.borrow(book)
        self.assertIn(book, user.get_borrowed_books())
        self.assertFalse(book.is_available())

        user.return_book(book)
        self.assertNotIn(book, user.get_borrowed_books())
        self.assertTrue(book.is_available())

    def test_library_add_find(self):
        lib = Library()
        book = Book("Книга", "Автор", 2000)
        lib.add_book(book)

        found = lib.find_book("Книга")
        self.assertIs(found, book)

        not_found = lib.find_book("Несуществующая")
        self.assertIsNone(not_found)

    def test_library_lend_and_return(self):
        lib = Library()
        user = User("Анна")
        book = Book("Книга", "Автор", 2000)

        lib.add_user(user)
        lib.add_book(book)

        lib.lend_book("Книга", "Анна")
        self.assertFalse(book.is_available())
        self.assertIn(book, user.get_borrowed_books())

        lib.return_book("Книга", "Анна")
        self.assertTrue(book.is_available())
        self.assertNotIn(book, user.get_borrowed_books())


if __name__ == "__main__":
    unittest.main()
