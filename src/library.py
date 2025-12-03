class Book:
    def __init__(self, title, author, year, available=True):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = available

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
        status = "доступна" if self.__available else "недоступна"
        return f"{self.__title} - {self.__author} ({self.__year}) - {status}"


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition, available=True):
        super().__init__(title, author, year, available)
        self.__pages = pages
        self.__condition = condition

    def repair(self):
        if self.__condition == "плохая":
            self.__condition = "хорошая"
        elif self.__condition == "хорошая":
            self.__condition = "новая"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format, available=True):
        super().__init__(title, author, year, available)
        self.__file_size = file_size
        self.__format = format

    def download(self):
        print(f"Книга {self.get_title()}.{self.__format} разме"
              f"ром {self.__file_size}МБ загружается...")


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.__borrowed_books.append(book)
            print(f"Вы успешно взяли книгу {book.get_title()}")
            book.mark_as_taken()
        else:
            print(f"Книга {book.get_title()} недоступна")

    def return_book(self, book):
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            print(f"Книга {book.get_title()} возвращена")
        else:
            print("У вас нет этой книги")

    def show_books(self):
        if self.__borrowed_books:
            print(f"Книги пользователя {self.name}:")
            for book in self.__borrowed_books:
                print(book)
        else:
            print(f"У пользователя {self.name} нет книг")

    def get_borrowed_books(self):
        return self.__borrowed_books


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)
        print(f"Книга {book.get_title()} добавлена в библиотеку")

    def remove_book(self, title):
        bt = self.find_book(title)
        if bt:
            self.__books.remove(bt)
            print(f"Книга {title} удалена из библиотеки")
        print(f"Книга '{title}' не найдена")

    def add_user(self, user):
        self.__users.append(user)
        print(f"Пользователь {user.name} зарегистрирован")

    def find_book(self, title):
        for book in self.__books:
            if book.get_title().lower() == title.lower():
                return book
        return "Книга не найдена"

    def find_user(self, name):
        for user in self.__users:
            if user.name.lower() == name.lower():
                return user
        return None

    def show_all_books(self):
        if self.__books:
            print("Все книги в библиотеке:")
            for i, book in enumerate(self.__books, 1):
                print(f"{i}. {book}")
        else:
            print("В библиотеке пока нет книг")

    def show_available_books(self):
        available_books = [book for book in
                           self.__books if book.is_available()]
        if available_books:
            print("Доступные книги:")
            for i, book in enumerate(available_books, 1):
                print(f"{i}. {book}")
        else:
            print("Нет доступных книг")

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)

        if not book:
            print(f'Книга {title} не найдена')
        elif not user:
            print(f'Пользователь {user_name} не найден')
        else:
            user.borrow(book)

    def return_book(self, title, user_name):

        book = self.find_book(title)
        user = self.find_user(user_name)

        if not book:
            print(f"Книга {title} не найдена")
        elif not user:
            print(f"Пользователь {user_name} не найден")
        else:
            user.return_book(book)


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)
