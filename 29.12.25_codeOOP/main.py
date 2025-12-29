from datetime import datetime


class Book:
    def __init__(self, book_id, title, author):
        self.__book_id = book_id
        self.__title = title
        self.__author = author
        self.is_available = True

    @property
    def book_id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def return_book(self):
        self.is_available = True

    def __str__(self):
        if self.is_available:
            status = "Available"
        else:
            status = "Borrowed"
        return f"[{self.book_id}] {self.title} by {self.author} - {status}"


class Member:
    def __init__(
        self,
        member_id,
        name,
    ):
        self.__member_id = member_id
        self.__name = name
        self.borrowed_books = []
        self.fine_balance = 0.0
        self.max_books = 3
        self.fine_rate = 5.0

    @property
    def member_id(self):
        return self.__member_id

    @property
    def name(self):
        return self.__name

    def borrow_book(self, book):
        if len(self.borrowed_books) >= self.max_books:
            print(f" {self.__name} reached limit")
            return False

        if book.borrow():
            self.borrowed_books.append(book)
            print(f" {self.__name} borrowed '{book.title}'")
            return True
        return False

    def return_book(self, book, days_late=0):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)

            if days_late > 0:
                fine = days_late * self.fine_rate
                self.fine_balance += fine
                print(f" Returned late. Fine: ${fine}")
            else:
                print(f" Returned on time")
            return True
        return False

    def pay_fine(self, amount):
        self.fine_balance -= amount
        print(f"Paid ${amount}. Balance: ${self.fine_balance}")

    def __str__(self):
        books = ", ".join([el.title for el in self.borrowed_books]) or "None"
        return f"{self.__name} (ID: {self.__member_id}) - Books: {books} | Fine: ${self.fine_balance}"


class StudentMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name)
        self.max_books = 3
        self.fine_rate = 2.0


class TeacherMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name)
        self.max_books = 5
        self.fine_rate = 2.0


class Reservation:
    def __init__(self, book, member):
        self.book = book
        self.member = member
        self.date_reserved = datetime.now()


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.reservations = []

    def add_book(self, book):
        self.books[book.book_id] = book
        print(f"added book: {book.title}")

    def add_member(self, member):
        self.members[member.member_id] = member
        print(f"added member: {member.name}")

    def borrow_book(self, member_id, book_id):
        member = self.members.get(member_id)
        book = self.books.get(book_id)
        if member and book:
            member.borrow_book(book)

    def return_book(self, member_id, book_id, days_late=0):
        member = self.members.get(member_id)
        book = self.books.get(book_id)
        if member and book:
            member.return_book(book, days_late)

    def reserve_book(self, member_id, book_id):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if member and book and not book.is_available:
            self.reservations.append(Reservation(book, member))
            print(f"Reserved '{book.title}' for {member.name}")

    def process_reservations(self):
        for el in self.reservations[:]:
            if el.book.is_available:
                print(f"{el.book.title} available for {el.member.name}")
                self.reservations.remove(el)

    def show_library_status(self):
        print("Liberary status:")
        print("\n BOOKS:")
        for el in self.books.values():
            print(f"{el}")
        print("\n MEMBERS:")
        for el in self.members.values():
            print(f"{el}")
        print("\n RESERVATIONS:", len(self.reservations))


if __name__ == "__main__":
    library = Library()
    # Add books
    b1 = Book(1, "1984", "George Orwell")
    b2 = Book(2, "Clean Code", "Robert Martin")
    b3 = Book(3, "Python Crash Course", "Eric Matthes")

    library.add_book(b1)
    library.add_book(b2)
    library.add_book(b3)

    # Add members
    m1 = StudentMember(1, "Anna")
    m2 = TeacherMember(2, "Dr. Smith")

    library.add_member(m1)
    library.add_member(m2)

    # Scenario
    library.borrow_book(1, 1)
    library.borrow_book(2, 2)
    library.reserve_book(2, 1)
    library.return_book(1, 1, days_late=3)
    library.process_reservations()
    m1.pay_fine(1.5)
    print("hello")

    library.show_library_status()
