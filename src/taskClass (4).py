"""
==============================================
  📚 ПРОЕКТ: СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ
==============================================
Цель:
Создать консольное приложение, моделирующее работу библиотеки
с использованием ООП-концепций: наследование, инкапсуляция,
полиморфизм и взаимодействие объектов.

----------------------------------------------
КЛАССЫ, КОТОРЫЕ НУЖНО РЕАЛИЗОВАТЬ:
----------------------------------------------

1. Класс Book (базовый)
   - Инкапсулированные атрибуты:
       __title, __author, __year, __available
   - Методы:
       get_title(), get_author(), get_year()
       is_available(), mark_as_taken(), mark_as_returned()
       __str__()

2. Класс PrintedBook(Book)
   - Дополнительные атрибуты:
       pages, condition ("новая", "хорошая", "плохая")
   - Методы:
       repair() — улучшает состояние книги

3. Класс EBook(Book)
   - Дополнительные атрибуты:
       file_size (МБ), format (pdf, epub, mobi)
   - Методы:
       download() — выводит сообщение о загрузке

4. Класс User
   - Атрибуты:
       name, __borrowed_books (инкапсулированный список)
   - Методы:
       borrow(book), return_book(book)
       show_books(), get_borrowed_books()

5. Класс Librarian(User) — наследник
   - Дополнительные методы:
       add_book(library, book)
       remove_book(library, title)
       register_user(library, user)

6. Класс Library
   - Инкапсулированные атрибуты:
       __books — список всех книг
       __users — список зарегистрированных пользователей
   - Методы:
       add_book(book), remove_book(title)
       add_user(user)
       find_book(title)
       show_all_books(), show_available_books()
       lend_book(title, user_name)
       return_book(title, user_name)

----------------------------------------------
ДОПОЛНИТЕЛЬНЫЕ ИДЕИ:
----------------------------------------------
- Ограничить количество книг у пользователя (не более 3)
- Добавить поиск по автору или году
- Реализовать сохранение данных в JSON
- Добавить класс AudioBook (наследник Book)
- Сделать меню (CLI) для управления библиотекой
----------------------------------------------
"""


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
        status = "доступна" if self.__available else "выдана"
        return f'"{self.__title}" - {self.__author} ({self.__year}) - {status}'


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

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, {self.pages} стр., состояние: {self.condition}"


class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format

    def download(self):
        print(f"Книга '{self.get_title()}' загружается...")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, {self.file_size} МБ, формат: {self.format}"


class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            return True
        return False

    def show_books(self):
        if not self.__borrowed_books:
            print(f"{self.name} не имеет взятых книг")
        else:
            print(f"Книги, взятые {self.name}:")
            for book in self.__borrowed_books:
                print(f"  - {book.get_title()}")

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
        print(f"Книга '{book.get_title()}' добавлена в библиотеку")

    def remove_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                self.__books.remove(book)
                print(f"Книга '{title}' удалена из библиотеки")
                return
        print(f"Книга '{title}' не найдена")

    def add_user(self, user):
        self.__users.append(user)
        print(f"Пользователь '{user.name}' зарегистрирован в библиотеке")

    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def show_all_books(self):
        if not self.__books:
            print("В библиотеке нет книг")
        else:
            print("Все книги в библиотеке:")
            for book in self.__books:
                print(f"  - {book}")

    def show_available_books(self):
        available_books = [
            book for book in self.__books
            if book.is_available()
        ]
        if not available_books:
            print("Нет доступных книг")
        else:
            print("Доступные книги:")
            for book in available_books:
                print(f"  - {book}")

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        user = self.__find_user(user_name)

        if not book:
            print(f"Книга '{title}' не найдена")
            return False

        if not user:
            print(f"Пользователь '{user_name}' не найден")
            return False

        if not book.is_available():
            print(f"Книга '{title}' уже выдана")
            return False

        if user.borrow(book):
            print(f"Книга '{title}' выдана пользователю '{user_name}'")
            return True
        else:
            print(f"Не удалось выдать книгу '{title}'")
            return False

    def return_book(self, title, user_name):
        book = self.find_book(title)
        user = self.__find_user(user_name)

        if not book:
            print(f"Книга '{title}' не найдена")
            return False

        if not user:
            print(f"Пользователь '{user_name}' не найден")
            return False

        if user.return_book(book):
            print(f"Книга '{title}' возвращена пользователем '{user_name}'")
            return True
        else:
            print(f"Пользователь '{user_name}' не брал книгу '{title}'")
            return False

    def __find_user(self, name):
        for user in self.__users:
            if user.name == name:
                return user
        return None


if __name__ == '__main__':
    lib = Library()

    # --- создаём книги ---
    b1 = PrintedBook("Война и мир", "Толстой", 1869, 1225, "хорошая")
    b2 = EBook("Мастер и Маргарита", "Булгаков", 1966, 5, "epub")
    b3 = PrintedBook(
        "Преступление и наказание",
        "Достоевский",
        1866,
        480,
        "плохая"
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
