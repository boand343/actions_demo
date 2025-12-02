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
        status = "доступна" if self.__available else "недоступна"
        return (f"'{self.__title}' - '{self.__author}' "
                f"({self.__year}), [{status}]")


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
            msg = (f"Книга '{self.get_title()}' отремонтирована. "
                   f"Состояние: {self.condition}")
            print(msg)
        elif self.condition == "хорошая":
            self.condition = "новая"
            msg = (f"Книга '{self.get_title()}' приведена в "
                   f"отличное состояние. Состояние: {self.condition}")
            print(msg)
        else:
            print(f"Книга '{self.get_title()}' новая")

    def __str__(self):
        return (super().__str__() +
                f" {self.pages} страниц. Состояние: {self.condition}")


class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format

    def download(self):
        msg = (f"Книга '{self.get_title()}' загружается... "
               f"[{self.file_size} МБ, формат {self.format}]")
        print(msg)

    def __str__(self):
        return (super().__str__() +
                f" {self.file_size} МБ. Формат: {self.format}")


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.__borrowed_books.append(book)
            book.mark_as_taken()
            print(f"{self.name} взял(а) книгу '{book.get_title()}'")
        else:
            msg = f"Книга '{book.get_title()}' недоступна для {self.name}"
            print(msg)

    def return_book(self, book):
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            print(f"{self.name} вернул(а) книгу '{book.get_title()}'")
        else:
            print(f"{self.name} не брал(а) эту книгу")

    def show_books(self):
        if self.__borrowed_books:
            print(f"\nКниги {self.name}:")
            for book in self.__borrowed_books:
                print(f"  - {book.get_title()} ({book.get_author()})")
        else:
            print(f"\n{self.name} пока не взял(а) никаких книг")

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()


class Librarian(User):
    def __init__(self, name):
        super().__init__(name)

    def add_book(self, library, book):
        library.add_book(book)
        msg = (f"Библиотекарь {self.name} добавил(а) книгу "
               f"'{book.get_title()}'")
        print(msg)

    def remove_book(self, library, title):
        library.remove_book(title)
        print(f"Библиотекарь {self.name} удалил(а) книгу '{title}'")

    def register_user(self, library, user):
        library.add_user(user)
        msg = (f"Библиотекарь {self.name} зарегистрировал(а) "
               f"пользователя {user.name}")
        print(msg)


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                self.__books.remove(book)
                print(f"Книга '{title}' удалена из библиотеки")
                return
        print(f"Книга '{title}' не найдена в библиотеке")

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def find_user(self, user_name):
        for user in self.__users:
            if user.name == user_name:
                return user
        return None

    def show_all_books(self):
        if self.__books:
            print("\nВСЕ КНИГИ В БИБЛИОТЕКЕ:")
            for book in self.__books:
                print(f"  - {book}")
        else:
            print("\nБиблиотека пуста")

    def show_available_books(self):
        available = [book for book in self.__books
                     if book.is_available()]
        if available:
            print("\nДОСТУПНЫЕ КНИГИ:")
            for book in available:
                print(f"  - {book}")
        else:
            print("\nДоступных книг нет")

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        if book and user:
            user.borrow(book)
        else:
            if not book:
                print(f"Книга '{title}' не найдена")
            if not user:
                print(f"Пользователь '{user_name}' не найден")

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = self.find_user(user_name)
        if book and user:
            user.return_book(book)
        else:
            if not book:
                print(f"Книга '{title}' не найдена")
            if not user:
                print(f"Пользователь '{user_name}' не найден")
