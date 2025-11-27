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
        return f"{self.__title}, {self.__author}, {self.__year}г."


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        conditions = ["плохая", "хорошая", "новая"]
        if self.condition != "новая":
            index = conditions.index(self.condition)
            self.condition = conditions[index + 1]
            print(f"Книга отремонтирована. Состояние книги: {self.condition}")
        else:
            print("Книга в новом состоянии")

    def __str__(self):
        return f"{super().__str__()}, \
            {self.pages} страниц, состояние книги: {self.condition}"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format

    def download(self):
        print(f"Загрузка электронной книги в формате {self.format}...")


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.__borrowed_books.append(book)
            book.mark_as_taken()
            print(f"Пользователь {self.name} взял книгу: {book.get_title()}")
        else:
            print("Книга недоступна.")

    def return_book(self, book):
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            print(f"Пользователь {self.name} вернул книгу: {book.get_title()}")

    def show_books(self):
        if len(self.__borrowed_books) == 0:
            print("У пользователя нет книг.")
        else:
            print("Книги пользователя:")
            for b in self.__borrowed_books:
                print('-', b)

    def get_borrowed_books(self):
        return list(self.__borrowed_books)


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

    def remove_book(self, title):
        self.__books = [b for b in self.__books if b.get_title() != title]

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for b in self.__books:
            if b.get_title() == title:
                return b
        return None

    def show_all_books(self):
        for b in self.__borrowed_books:
            print('-', b)

    def show_available_books(self):
        for b in self.__books:
            if b.is_available():
                print(b)

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = next((u for u in self.__users if u.name == user_name), None)

        if book and user:
            user.borrow(book)
        else:
            print("Ошибка выдачи книги.")

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = next((u for u in self.__users if u.name == user_name), None)

        if book and user:
            user.return_book(book)
        else:
            print("Ошибка возврата книги.")


if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook(
        "Мастер и Маргарита",
        "Булгаков",
        1966,
        5,
        "epub",
    )
    b3 = PrintedBook(
        "Преступление и наказание",
        "Достоевский",
        1866,
        480,
        "плохая",
    )

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
