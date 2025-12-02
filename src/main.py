'''def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


if __name__ == "__main__":
    print("2 + 3 =", add(2, 3))'''

class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def is_available(self):
        return self.__available

    def mark_as_taken(self):
        self.__available = False

    def mark_as_returned(self):
        self.__available = True

    def __str__(self):
        if self.__available:
            status = "доступна"
        else:
            status = "книги нет"
        return f"Title: {self.__title} Author: {self.__author} Year: {self.__year} Status: {status}"


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self._pages = pages
        self._condition = condition

    def repair(self):
        if self._condition == "плохая":
            self._condition = "хорошая"
            return "сделали из плохой, хорошую"
        elif self._condition == "хорошая":
            return "Книга уже в хорошем состоянии"
        else:
            return "Книга новая"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format_):
        super().__init__(title, author, year)
        self._file_size = file_size
        self._format = format_

    def download(self):
        print(f"Книга {self.get_title()} загружается... размер {self._file_size} МБ")


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f"Пользователь {self.name} взял книгу {book.get_title()}")
        else:
            print(f"Книга {book.get_title()} недоступна")

    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(f"Пользователь {self.name} вернул книгу {book.get_title()}")
        else:
            print(f"У пользователя {self.name} нет книги")

    def show_books(self):
        if self.__borrowed_books:
            number = 1
            for book in self.__borrowed_books:
                print(f"{number}. {book.get_title()}")
                number += 1
        else:
            print(f"{self.name} не брал книг")

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)
        print(f"Книга {book.get_title()} добавлена")

    def remove_book(self, title):
        book = self.find_book(title)
        if book in self.__books:
            self.__books.remove(book)
            print(f"Книга {title} удалена из библиотеки")

    def add_user(self, user):
        self.__users.append(user)
        print(f"Пользователь {user.name} добавлен")

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self):
        number = 1
        for book in self.__books:
            print(f"{number}. {book.get_title()}")
            number += 1

    def show_available_books(self):
        number = 1
        for book in self.__books:
            if book.is_available():
                print(f"{number}. {book.get_title()}")
                number += 1

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            print(f"книга {title} не найдена")
            return

        user = None
        for u in self.__users:
            if u.name == user_name:
                user = u
                break

        if not user:
            print(f"Пользователь {user_name} не найден")
            return

        user.borrow(book)

    def return_book(self, title, user_name):
        user = None
        for u in self.__users:
            if u.name == user_name:
                user = u
                break
        if not user:
            print(f"Пользователь {user_name} не найден")
            return

        for book in user.get_borrowed_books():
            if book.get_title() == title:
                user.return_book(book)
                return
        print(f"Книга {title} у пользователя {user_name} не найдена")


if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook("Преступление и наказание", "Достоевский", 1866, 480, "плохая")

    # --- создаём пользователей ---
    user1 = User("Анна")
    librarian = Librarian("Мария")

    # --- библиотекарь добавляет книги ---
    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    # --- библиотекарь регистрирует пользователя ---
    librarian.register_user(lib, user1)

    # --- пользователь берёт книгу ---
    lib.lend_book("Война и мир", "Анна")

    # --- пользователь смотрит свои книги ---
    user1.show_books()

    # --- возвращает книгу ---
    lib.return_book("Война и мир", "Анна")

    # --- электронная книга ---
    b2.download()

    # --- ремонт книги ---
    b3.repair()
    print(b3)
