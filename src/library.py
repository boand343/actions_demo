class Book:
    def __init__(self,name,author,y):
        self.__title = name
        self.__author = author
        self.__year = y
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
            s='Книга доступна'
        else:
            s='Книга не доступна'
        return f"Название: {self.__title}, Автор: {self.__author}, Год: {self.__year}, Статус: {s}"




class PrintedBook(Book):
    def __init__(self,name,author,y,pages,condition):
        super().__init__(name, author, y)
        self.__pages = pages
        self.__condition = condition
    def repair(self):
        if self.__condition == "плохая":
            self.__condition = "хорошая"
    def __str__(self):
        osn = super().__str__()
        return f"{osn}, Кол-во страниц: {self.__pages}, Cостояние: {self.__condition}"

class EBook(Book):
    def __init__(self,name, author, y,file_size,format):
        super().__init__(name, author, y)
        self.__file_size = file_size
        self.__format = format
    def download(self):
        print(f'Книга {self.get_title()} загружается...')
    def __str__(self):
        osn = super().__str__()
        return f"{osn}, Объём: {self.__file_size}, Формат: {self.__format}"



class User:
    def __init__(self,name):
        self.name = name
        self.__borrowed_books = []
    def borrow(self,book):

        if book.is_available():
            book.mark_as_taken()
            self.__borrowed_books.append(book)
            return True
        return False
    def return_book(self,book):

        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)
            book.mark_as_returned()
            return True
        return False
    def show_books(self):
        if len(self.__borrowed_books)!=0:
            for book in self.__borrowed_books:
                print(book.get_title())
        else:
            print("нету книг")

    def get_borrowed_books(self):
        return self.__borrowed_books

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
        for book in self.__books:
            if book.get_title() == title:
                self.__books.remove(book)
                return True
        return False
    def add_user(self, user):
        self.__users.append(user)
    def find_book(self, title):
        for book in self.__books:
            if book.get_title() == title:
                return book
        return None
    def show_all_books(self):
        for book in self.__books:
            print(book.get_title())
    def show_available_books(self):

        for book in self.__books:
            if book.is_available():
                print(book.get_title())

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            return False

        for user in self.__users:
            if user.name == user_name:

                return user.borrow(book)
        return False
    def return_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            return False
        for user in self.__users:
            if user.name == user_name:

                return user.return_book(book)
        return False



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