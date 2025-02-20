import os
import mysql.connector as mys

# Database Connection
mycon = mys.connect(
    host="localhost", user="root", passwd="Yksrocks", database="book_store_management"
)
mycur = mycon.cursor()

if mycon.is_connected():
    print("\nSuccessfully connected to the database")


def delete_empty_books():
    """Delete books with zero quantity."""
    query = "DELETE FROM books WHERE Numbers_of_book <= 0"
    mycur.execute(query)
    mycon.commit()


def print_separator():
    print("\n\t\t========================================\n")


def login():
    """User login function."""
    while True:
        username = input(" USER NAME  ---  ")
        password = input(" PASSWORD  ---  ")

        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        mycur.execute(query, (username, password))
        user = mycur.fetchone()

        if user:
            print("\nLogin Successful!\n")
            break
        else:
            print_separator()
            print(" Username or Password is Incorrect. Try Again")
            print_separator()


def view_all_books():
    """Displays all available books."""
    print("\u0332".join("BOOK NAMES~~"))
    print("------------------------------------")

    query = "SELECT Name FROM books"
    mycur.execute(query)
    books = mycur.fetchall()

    if books:
        for index, book in enumerate(books, start=1):
            print(f"{index} --> {book[0]}")
    else:
        print("No books available")


def check_book_availability(book_name):
    """Checks if a book is available and returns its data."""
    query = "SELECT * FROM books WHERE Name = %s"
    mycur.execute(query, (book_name,))
    return mycur.fetchone()


def purchase_book(book_name, quantity=1):
    """Handles book purchase logic."""
    book = check_book_availability(book_name)

    if not book:
        print_separator()
        print("SORRY, NO BOOK WITH THIS NAME EXISTS / INCORRECT NAME")
        return

    available_quantity = book[6]

    if available_quantity < quantity:
        print("\nYou can't buy that many books.")
        print(f"But you can buy up to {available_quantity} books.\n")
        return

    query = "UPDATE books SET Numbers_of_book = Numbers_of_book - %s WHERE Name = %s"
    mycur.execute(query, (quantity, book_name))
    mycon.commit()

    print("\nBook successfully purchased!")
    remaining_books = available_quantity - quantity
    if remaining_books <= 8:
        print("\nWARNING: Low stock! Only", remaining_books, "left.")
    else:
        print("\nBooks left:", remaining_books)


def add_book():
    """Adds a new book to the database."""
    num_books = int(input("ENTER NO. OF BOOKS TO ADD -- "))

    for _ in range(num_books):
        SNo = int(input("ENTER SNo OF BOOK -- "))
        name = input("ENTER NAME OF BOOK --- ")
        author = input("ENTER NAME OF AUTHOR -- ")
        year = int(input("ENTER YEAR OF PUBLISHING -- "))
        ISBN = input("ENTER ISBN OF BOOK -- ")
        price = int(input("ENTER PRICE OF BOOK -- "))
        quantity = int(input("ENTER NO. OF BOOKS -- "))

        # Check if ISBN exists
        query = "SELECT * FROM books WHERE ISBN = %s"
        mycur.execute(query, (ISBN,))
        if mycur.fetchone():
            print("This ISBN already exists. Try again.")
            return

        # Insert new book
        query = "INSERT INTO books (SNo, Name, Author, Year, ISBN, Price, Numbers_of_book) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mycur.execute(query, (SNo, name, author, year, ISBN, price, quantity))
        mycon.commit()

        print("\nBook added successfully!")


def update_book():
    """Updates an existing book record."""
    ISBN = input("ENTER ISBN OF BOOK TO UPDATE -- ")

    query = "SELECT * FROM books WHERE ISBN = %s"
    mycur.execute(query, (ISBN,))
    book = mycur.fetchone()

    if not book:
        print("\nNo book found with this ISBN.")
        return

    SNo = int(input("ENTER NEW SNo OF BOOK -- "))
    name = input("ENTER NEW NAME OF BOOK --- ")
    author = input("ENTER NEW AUTHOR -- ")
    year = int(input("ENTER NEW YEAR OF PUBLISHING -- "))
    new_ISBN = input("ENTER NEW ISBN OF BOOK -- ")
    price = int(input("ENTER NEW PRICE OF BOOK -- "))
    quantity = int(input("ENTER NEW NO. OF BOOKS -- "))

    query = "UPDATE books SET SNo = %s, Name = %s, Author = %s, Year = %s, ISBN = %s, Price = %s, Numbers_of_book = %s WHERE ISBN = %s"
    mycur.execute(query, (SNo, name, author, year, new_ISBN, price, quantity, ISBN))
    mycon.commit()

    print("\nBook updated successfully!")


def delete_book():
    """Deletes a book from the database."""
    ISBN = input("ENTER ISBN OF THE BOOK TO DELETE -- ")

    query = "SELECT * FROM books WHERE ISBN = %s"
    mycur.execute(query, (ISBN,))
    book = mycur.fetchone()

    if not book:
        print("\nNo book found with this ISBN.")
        return

    confirm = input("ARE YOU SURE YOU WANT TO DELETE THIS BOOK? (Y/N) -- ").lower()
    if confirm == "y":
        query = "DELETE FROM books WHERE ISBN = %s"
        mycur.execute(query, (ISBN,))
        mycon.commit()
        print("\nBook deleted successfully!")
    else:
        print("\nBook not deleted.")


# Main Menu
while True:
    print("\n\t\tBook Store Management System")
    print("\t\t--------------------------------")
    print("     * TO VIEW ALL BOOKS, ENTER 1")
    print("     * TO SEARCH AND BUY A BOOK, ENTER 2")
    print("     * TO ADD A BOOK, ENTER 3")
    print("     * TO UPDATE A BOOK, ENTER 4")
    print("     * TO DELETE A BOOK, ENTER 5")
    print("     * TO EXIT, ENTER 6")

    choice = input("\nENTER YOUR CHOICE -- ")

    if choice == "1":
        view_all_books()
    elif choice == "2":
        book_name = input("ENTER BOOK NAME ---- ")
        purchase_book(book_name)
    elif choice == "3":
        add_book()
    elif choice == "4":
        update_book()
    elif choice == "5":
        delete_book()
    elif choice == "6":
        print("\nExiting program...")
        mycur.close()
        mycon.close()
        os._exit(0)
    else:
        print("\nInvalid choice! Please try again.")

    delete_empty_books()  # Remove books with zero quantity after each transaction

    restart = input("\nDo you want to restart? (yes/no) -- ").lower()
    if restart != "yes":
        print("\nExiting program...")
        mycur.close()
        mycon.close()
        os._exit(0)
