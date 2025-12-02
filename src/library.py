class Book:
    """
        __title (str)     — название
        __author (str)    — автор
        __year (int)      — год издания
        __available (bool)— флаг доступности (True/False)
    """

    def __init__(self, title: str, author: str, year: int) -> None:
        self.__title = title
        self.__author = author
        self.__year = year
        self.__available = True

    # --- Геттеры ---
    def get_title(self) -> str:
        return self.__title

    def get_author(self) -> str:
        return self.__author

    def get_year(self) -> int:
        return self.__year

    # --- Доступность ---
    def is_available(self) -> bool:
        return self.__available

    # --- Изменение статуса ---
    def mark_as_taken(self) -> None:
        self.__available = False

    def mark_as_returned(self) -> None:
        self.__available = True

    def __str__(self) -> str:
        state = "доступна" if self.__available else "недоступна"
        return (
            f"«{self.__title}» — {self.__author}, "
            f"{self.__year} ({state})"
        )


class PrintedBook(Book):
    """Бумажная книга."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        condition: str,
    ) -> None:
        super().__init__(title, author, year)
        self.pages = int(pages)
        self.condition = condition

    def repair(self) -> None:
        ladder = ["плохая", "хорошая", "новая"]
        if self.condition in ladder:
            idx = ladder.index(self.condition)
            if idx < len(ladder) - 1:
                self.condition = ladder[idx + 1]
        print(
            f"Книга «{self.get_title()}» теперь "
            f"{self.condition}."
        )

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | {self.pages} стр., "
            f"состояние: {self.condition}"
        )


class EBook(Book):
    """Электронная книга."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        file_size: int | float,
        format_: str,
    ) -> None:
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format_

    def download(self) -> None:
        print(f"Книга «{self.get_title()}» загружается...")

    def __str__(self) -> str:
        return (
            f"{super().__str__()} | {self.file_size} МБ, "
            f"формат: {self.format}"
        )


class User:
    """Описываем читателя библиотеки."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.__borrowed_books: list[Book] = []

    def borrow(self, book: Book) -> None:
        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            print(
                f"{self.name} взял(а) книгу "
                f"«{book.get_title()}»."
            )
        else:
            print(
                f"Книга «{book.get_title()}» "
                f"недоступна."
            )

    def return_book(self, book: Book) -> None:
        if book in self.__borrowed_books:
            book.mark_as_returned()
            self.__borrowed_books.remove(book)
            print(
                f"{self.name} вернул(а) книгу "
                f"«{book.get_title()}»."
            )
        else:
            print(
                f"{self.name} не имеет книги "
                f"«{book.get_title()}»."
            )

    def show_books(self) -> None:
        if not self.__borrowed_books:
            print(f"{self.name} не имеет книг.")
        else:
            print(f"Книги {self.name}:")
            for book in self.__borrowed_books:
                print(f" - {book.get_title()}")

    def get_borrowed_books(self) -> tuple[Book, ...]:
        return tuple(self.__borrowed_books)


class Librarian(User):
    """Может управлять библиотекой."""

    def add_book(self, library: "Library", book: Book) -> None:
        library.add_book(book)
        print(
            f"Библиотекарь {self.name} добавил(а) книгу "
            f"«{book.get_title()}»."
        )

    def remove_book(self, library: "Library", title: str) -> None:
        if library.remove_book(title):
            print(
                f"Библиотекарь {self.name} удалил(а) книгу "
                f"«{title}»."
            )
        else:
            print(f"Книга «{title}» не найдена.")

    def register_user(self, library: "Library", user: User) -> None:
        library.add_user(user)
        print(
            "Библиотекарь "
            f"{self.name} зарегистрировал(а) пользователя "
            f"{user.name}."
        )


class Library:
    """Хранит коллекцию книг и пользователей."""

    def __init__(self) -> None:
        self.__books: list[Book] = []
        self.__users: list[User] = []

    def add_book(self, book: Book) -> None:
        self.__books.append(book)

    def remove_book(self, title: str) -> bool:
        book = self.find_book(title)
        if book:
            self.__books.remove(book)
            return True
        return False

    def add_user(self, user: User) -> None:
        self.__users.append(user)

    def find_book(self, title: str) -> Book | None:
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None

    def __find_user(self, name: str) -> User | None:
        for user in self.__users:
            if user.name == name:
                return user
        return None

    def show_all_books(self) -> None:
        print("Все книги в библиотеке:")
        if not self.__books:
            print(" - (пусто)")
        for book in self.__books:
            print(" -", book)

    def show_available_books(self) -> None:
        print("Доступные книги:")
        available = [book for book in self.__books if book.is_available()]
        if not available:
            print(" - (нет доступных)")
        for book in available:
            print(" -", book)

    def lend_book(self, title: str, user_name: str) -> None:
        book = self.find_book(title)
        user = self.__find_user(user_name)
        if not book or not user:
            print("Книга или пользователь не найдены.")
            return
        user.borrow(book)

    def return_book(self, title: str, user_name: str) -> None:
        book = self.find_book(title)
        user = self.__find_user(user_name)
        if not book or not user:
            print("Книга или пользователь не найдены.")
            return
        user.return_book(book)


# Пример использования
if __name__ == "__main__":
    lib = Library()

    b1 = PrintedBook(
        "Война и мир",
        "Толстой",
        1869,
        1225,
        "хорошая",
    )
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
