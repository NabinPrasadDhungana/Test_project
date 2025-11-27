class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def view_book_info(self):
        print(f"Book id: {self.book_id}, Title: {self.title}, Author: {self.author}, Quantity: {self.quantity}")

    def check_availability(self):
        return self.quantity
    
    def update_quantity(self, quantity):
        self.quantity += quantity
    
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.check_availability() > 0:
            self.borrowed_books.append(book)
            book.update_quantity(-1)
            print(f"Borrowed book '{book.title}'")
        else:
            print(f"Book '{book.title}' not available!")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_quantity(1)
            print(f"Book '{book.title}' returned!")
        else:
            print(f"{self.name} does not have '{book.title}' borrowed!")

    def view_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name} has borrowed the following books:")
            for book in self.borrowed_books:
                print(f"- {book.title}")
        else:
            print(f"{self.name} hasn't borrowed any books.")

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def list_books(self):
        if self.books:
            print("The following are the list of books:")
            for book in self.books:
                print(f"- {book.title}")
        else:
            print("There are no books in the library!")
    
    def search_book_by_title(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        return found_books
    
    def add_new_book_by_user(self):
        book_id = int(input("Enter a book_id: "))
        if any(book_id == book.book_id for book in self.books):
            print("Book with the same book ID already exists!")
            return
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        quantity = int(input("Enter the quantity of books to be added: "))

        new_book = Book(book_id=book_id, title=title, author=author, quantity=quantity)
        self.add_book(new_book)
        print(f"New book '{new_book.title}' added to the library.")
        
    def register_member(self, member):
        if any(current_user.member_id == member.member_id for current_user in self.members):
            print("The member with the same ID already exists!")
            return
        self.members.append(member)
        print(f"'{member.name}' added to the library.")


library = Library()

book1 = Book(1, "Ramayan", "Balmiki", 2)
book2 = Book(2, "Mahabharat", "Ved Vyas", 3)
book3 = Book(3, "Shree Swasthani", "Unknown", 1)

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

user1 = Member(1, "Sameer Kshetri")
user2 = Member(2, "Nabin Prasad Dhungana")

library.register_member(user1)
library.register_member(user2)

while True:
    print("You have the following operations:")
    print("1. View all books  2. Add books")
    print("3. Search a book   4. Borrow a book")
    print("5. Return a book   6. View borrowed books")
    print("7. Add new member    8. Exit")

    choice = input("Enter you choice: ")

    if choice == '1':
        library.list_books()

    elif choice == '2':
        library.add_new_book_by_user()

    elif choice == '3':
        title = input("Enter the book title to search: ")
        found_books = library.search_book_by_title(title)
        if found_books:
            for book in found_books:
                print(f"- {book.title}")
        else:
            print("There is no such book in the library.")

    elif choice == '4':
        member_id = int(input("Enter the member id: "))
        book_id = int(input("Enter the book id: "))
        member = next((member for member in library.members if member.member_id == member_id), None)

        book = next((book for book in library.books if book.book_id == book_id), None)

        if member and book:
            member.borrow_book(book)
        else:
            print("Either member or book id is invalid.")

    elif choice == '5':
        member_id = int(input("Enter the member id: "))
        book_id = int(input("Enter the book id: "))
        member = next((member for member in library.members if member.member_id == member_id), None)

        book = next((book for book in library.books if book.book_id == book_id), None)

        if member and book:
            member.return_book(book)
        else:
            print("Either member or book id is invalid.")

    elif choice == '6':
        member_id = int(input("Enter member id: "))

        member = next((member for member in library.members if member.member_id == member_id), None)

        if member:
            member.view_borrowed_books()
        else:
            print("Provided user id is invalid.")

    elif choice == '7':
        member_id = int(input("Enter user id: "))
        name = input("Enter name of user: ")
        user = Member(member_id, name)

        library.register_member(user)

    elif choice == '8':
        print("Exiting...")
        break

    else:
        print("Enter a valid choice.")
