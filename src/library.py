import json


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
        return f"{self.__title} ({self.__author}, {self.__year}) - {status}"


class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition

    def repair(self):
        if self.condition == "плохая":
            self.condition = "хорошая"
        elif self.condition == "хорошая":
            self.condition = "новая"
        print(
            f"Состояние книги '{self.get_title()}' теперь: "
            f"{self.condition}"
        )

    def __str__(self):
        return (
            f"{super().__str__()} - {self.pages} стр., "
            f"состояние: {self.condition}"
        )


class EBook(Book):
    def __init__(self, title, author, year, file_size, file_format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = file_format

    def download(self):
        print(f"Книга '{self.get_title()}' загружается...")

    def __str__(self):
        return (
            f"{super().__str__()} - {self.file_size} МБ, "
            f"формат: {self.format}"
        )


class AudioBook(Book):
    def __init__(self, title, author, year, duration):
        super().__init__(title, author, year)
        self.duration = duration

    def __str__(self):
        return f"{super().__str__()} - аудио {self.duration} мин"


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if len(self.__borrowed_books) >= 3:
            print(f"{self.name} не может взять больше 3 книг.")
            return

        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(f"{self.name} взял книгу '{book.get_title()}'")
        else:
            print(f"Книга '{book.get_title()}' недоступна")

    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(f"{self.name} вернул книгу '{book.get_title()}'")
        else:
            print(f"{self.name} не брал книгу '{book.get_title()}'")

    def show_books(self):
        if self.__borrowed_books:
            print(f"Книги {self.name}:")
            for b in self.__borrowed_books:
                print(" •", b)
        else:
            print(f"{self.name} не взял ни одной книги")

    def get_borrowed_books(self):
        return list(self.__borrowed_books)


class Librarian(User):
    def add_book(self, library, book):
        library.add_book(book)
        print(f"Библиотекарь добавил книгу '{book.get_title()}'")

    def remove_book(self, library, title):
        library.remove_book(title)

    def register_user(self, library, user):
        library.add_user(user)
        print(f"Пользователь '{user.name}' зарегистрирован")


class Library:
    def __init__(self):
        self.__books = []
        self.__users = []

    def add_book(self, book):
        self.__books.append(book)

    def remove_book(self, title):
        book = self.find_book(title)
        if book:
            self.__books.remove(book)
            print(f"Книга '{title}' удалена")
        else:
            print("Такой книги нет")

    def add_user(self, user):
        self.__users.append(user)

    def find_book(self, title):
        for b in self.__books:
            if b.get_title() == title:
                return b
        return None

    def find_user(self, name):
        for u in self.__users:
            if u.name == name:
                return u
        return None

    def show_all_books(self):
        print("\nВсе книги:")
        for b in self.__books:
            print(" •", b)

    def show_available_books(self):
        print("\nДоступные книги:")
        for b in self.__books:
            if b.is_available():
                print(" •", b)

    def search_by_author(self, author):
        print(f"\nПоиск по автору: {author}")
        for b in self.__books:
            if b.get_author() == author:
                print(" •", b)

    def search_by_year(self, year):
        print(f"\nПоиск по году: {year}")
        for b in self.__books:
            if b.get_year() == year:
                print(" •", b)

    def lend_book(self, title, user_name):
        user = self.find_user(user_name)
        book = self.find_book(title)
        if user and book:
            user.borrow(book)
        else:
            print("Ошибка: пользователь или книга не найдены")

    def return_book(self, title, user_name):
        user = self.find_user(user_name)
        book = self.find_book(title)
        if user and book:
            user.return_book(book)
        else:
            print("Ошибка: пользователь или книга не найдены")

    def save_to_json(self, filename):
        data = {
            "books": [b.get_title() for b in self.__books],
            "users": [u.name for u in self.__users],
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Данные сохранены в JSON")

    def load_from_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Данные загружены:", data)


if __name__ == "__main__":
    lib = Library()

    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook(
        "Преступление и наказание", "Достоевский", 1866, 480, "плохая"
    )

    user1 = User("Анна")
    librarian = Librarian("Мария")

    librarian.add_book(lib, b1)
    librarian.add_book(lib, b2)
    librarian.add_book(lib, b3)

    librarian.register_user(lib, user1)

    lib.lend_book("Война и мир", "Анна")

    user1.show_books()

    lib.return_book("Война и мир", "Анна")

    b2.download()

    b3.repair()
    print(b3)