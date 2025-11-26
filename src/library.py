import json


class Book:
    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year

    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_info(self):
        return [self.__title, self.__author, self.__year]

    def __str__(self):
        return f'"{self.__title}" - {self.__author} ({self.__year})'
    
class PrintedBook(Book):
    def __init__(self, title, author, year, pages, condition):
        super().__init__(title, author, year)
        self.pages = pages
        self.condition = condition
        self.available = None
        self.type = 0

    def get_type(self):
        return self.type

    def repair(self):
        if self.condition == 'bad':
            self.condition = 'good'
        elif self.condition == 'good':
            self.condition = 'new'
        else:
            print(f'error: {self.get_title()} can\'t be repaired')

    def is_available(self):
        return False if self.available else True
    
    def taken_by(self):
        return self.available if self.available else None
    
    def mark_as_taken(self, name):
        self.available = name
    
    def mark_as_returned(self):
        self.available = None

    def get_info(self):
        return [self.type] + super().get_info() + [self.pages, self.condition, self.available]

    def __str__(self):
        return f'{super().__str__()} [{self.pages} pages, condition: {self.condition}, {'unavailable' if self.available else 'available'}]'
    
class EBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format
        self.type = 1

    def get_type(self):
        return self.type

    def download(self):
        print(f'Start downloading "{self.get_title()}"')

    def get_info(self):
        return [self.type] + super().get_info() + [self.file_size, self.format]
    
    def __str__(self):
        return f'{super().__str__()} [{self.file_size} Mb, {self.format}]'
    
class AudioBook(Book):
    def __init__(self, title, author, year, file_size, format):
        super().__init__(title, author, year)
        self.file_size = file_size
        self.format = format
        self.type = 2

    def get_type(self):
        return self.type

    def download(self):
        print(f'Start downloading "{self.get_title()}"')

    def get_info(self):
        return [self.type] + super().get_info() + [self.file_size, self.format]
    
    def __str__(self):
        return f'{super().__str__()} [{self.file_size} Mb, {self.format}]'
    
class User:
    def __init__(self, name):
        self.name = name
        self.__borrowed_books = []

    def borrow(self, book):
        if len(self.__borrowed_books) < 3:
            if not book.get_type():
                if book.is_available():
                    book.mark_as_taken(self.name)
                    self.__borrowed_books.append(book)
                else:
                    print(f'{book.get_title()} is unavailable')
            else:
                print(f'{self.name} can\'t borrow {book.get_title()}, book\'s type: {'EBook' if book.get_type() == 1 else 'AudioBook'}')
        else:
            print(f'{self.name} has already taken 3 books')
    
    def return_book(self, book):
        if book in self.__borrowed_books:
            if not book.is_available():
                book.mark_as_returned()
                self.__borrowed_books.remove(book)
        else:
            print(f'{self.name} didn\'t borrow {book.get_title()}')
    
    def show_books(self):
        if self.__borrowed_books:
            return [i.get_title() for i in self.__borrowed_books]
        
    def _restore_borrowed_books(self, books):
        self.__borrowed_books.append(books)

class Librarian(User):
    def __init__(self, library, name):
        super().__init__(name)
        library.add_librarian(name)

    def add_book(self, library, book):
        library.add_book(book)
        print(f'{self.name} added "{book.get_title()}"')

    def remove_book(self, library, title):
        library.remove_book(title)
        print(f'{self.name} deleted "{title}"')

    def register_user(self, library, user):
        library.add_user(user)
        print(f'{self.name} added user {user.name}')

class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__librarians = []

    def add_book(self, book):
        self.__books.append(book)
    
    def remove_book(self, title):
        book = self.find_book(title)
        if type(book) == list and len(book):
            book = book[int(input('choose book:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j}' for i, j in enumerate(book)]) + '\n> '))-1]

        if book:
            self.__books.remove(book)
        else:
            print('Book wasn\'t found')

    def add_user(self, user):
        self.__users.append(user)

    def remove_user(self, name):
        user = self.find_user(name)
        if type(user) == list and len(user):
            user = user[int(input('choose user:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j}' for i, j in enumerate(user)]) + '\n> '))-1]

        if user:
            self.__users.remove(user)
        else:
            print('User wasn\'t found')

    def add_librarian(self, librarian):
        self.__librarians.append(librarian)

    def remove_librarian(self, name):
        if name in self.__librarians:
            self.__librarians.remove(name)
        else:
            print('Librarian wasn\'t found')
    
    def find_book(self, title=None, author=None, year=None):
        books = []
        if title:
            for i in self.__books:
                if i.get_title() == title:
                    books.append(i)
        elif author:
            for i in self.__books:
                if i.get_author() == author:
                    books.append(i)
        else:
            for i in self.__books:
                if i.get_year() == year:
                    books.append(i)
        return books[0] if len(books) == 1 else books
    
    def find_user(self, name):
        users = []
        for i in self.__users:
            if i.name == name:
                users.append(i)
        return users[0] if len(users) == 1 else users
    
    def show_all_books(self):
        dt = {}
        for i in self.__books:
            title = i.get_title()
            if title in dt:
                dt[i.get_title()] = dt[i.get_title()] + [i.get_info()]
            else:
                dt[i.get_title()] = [i.get_info()]
        return dt
    
    def show_all_users(self):
        dt = {}
        for i in self.__users:
            dt[i.name] = i.show_books()
        return dt
    
    def show_all_librarians(self):
        return [i for i in self.__librarians]
    
    def show_available_books(self):
        return [i for i in self.__books if i.is_available()]

    def lend_book(self, title, user_name):
        book = self.find_book(title)
        if type(book) == list and len(book):
            book = book[int(input('choose book:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j}' for i, j in enumerate(book) if not j.get_type() and j.is_available()]) + '\n> '))-1]
        user = self.find_user(user_name)
        if type(user) == list and len(user):
            user = user[int(input('choose user:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j.name}' for i, j in enumerate(user)]) + '\n> '))-1]

        if book:
            if user:
                user.borrow(book)
            else:
                print(f'{user_name} not found')
        else:
            print(f'"{title}" not found')

    def return_book(self, title, user_name):
        book = self.find_book(title)
        if not book:
            print(f'"{title}" not found')
            return
        if type(book) == list and len(book):
            book = book[int(input('choose book:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j}' for i, j in enumerate(book) if not j.get_type()]) + '\n> '))-1]
        user = self.find_user(user_name)
        if type(user) == list and len(user):
            user = user[int(input('choose user:\n' + '\n'.join([f'{'  ' + str(i+1)}. {j.name}' for i, j in enumerate(user)]) + '\n> '))-1]

        if user:
            print(user.show_books())
            if title in user.show_books():
                if type(book) == list and len(book):
                    for i in book:
                        if not i.get_type() and i.taken_by() == user.name:
                            user.return_book(i)
                else:
                    user.return_book(book)
            else:
                print(f'{user_name} didn\'t borrow "{title}"')
        else:
            print(f'{user_name} not found')

    def load_data(self, data):
        self.__books = []
        self.__users = []
        self.__librarians = []

        self.__librarians = data["librarians"]

        users_map = {}
        for username in data["users"].keys():
            user = User(username)
            self.__users.append(user)
            users_map[username] = user

        for title, items in data["books"].items():
            for info in items:
                book_type = info[0]

                if book_type == 0:
                    _, title, author, year, pages, condition, available = info
                    book = PrintedBook(title, author, year, pages, condition)
                    book.available = available
                elif book_type == 1:
                    _, title, author, year, file_size, fmt = info
                    book = EBook(title, author, year, file_size, fmt)
                elif book_type == 2:
                    _, title, author, year, file_size, fmt = info
                    book = AudioBook(title, author, year, file_size, fmt)
                else:
                    continue

                self.__books.append(book)

        for book in self.__books:
            if not book.get_type() and not book.is_available():
                username = book.taken_by()
                user = users_map.get(username)
                if user:
                    user._restore_borrowed_books(book)

    def to_dict(self):
        return {
            'librarians': self.show_all_librarians(),
            'users': self.show_all_users(),
            'books': self.show_all_books()
        }

    def save_to_file(self, filename):
        data = self.to_dict()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    lib = Library()

    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        lib.load_data(data)
    except FileNotFoundError:
        data = {'librarians': [], 'users': {}, 'books': {}}

    ###

    lib.save_to_file('data.json')