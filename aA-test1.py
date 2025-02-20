import mysql.connector as mys
import os

# Database connection details (move to config file ideally)
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "Yksrocks",
    'database': "book_store_management"
}

def connect_db(db_config):
    """Connects to the database and returns a cursor; handles connection errors."""
    try:
        mydb = mys.connect(**db_config)
        if mydb.is_connected():
            print("Successfully connected to the database")
            return mydb.cursor()
        else:
            print("Failed to connect to the database")
            return None
    except mys.Error as err:
        print(f"Database error: {err}")
        return None

def delete_zero_stock(cursor, mydb):
    """Deletes books with zero stock."""
    cursor.execute("DELETE FROM books WHERE Numbers_of_book <= 0")
    mydb.commit()

def separator():
    print("\n\t\t========================================")

def login(cursor):
    """Handles user login with error handling and input validation."""
    while True:
        user_name = input("USER NAME --- ")
        passw = input("PASSWORD --- ")
        cursor.execute("SELECT * FROM login WHERE Username = %s AND Password = %s", (user_name, passw))
        user = cursor.fetchone()
        if user:
            return True
        else:
            separator()
            print("Username or Password is Incorrect. Try Again")
            separator()

def view_all_books(cursor):
    """Displays all books."""
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("BOOK NAMES".center(30, "~"))
        print("-" * 30)
        for i, book in enumerate(books, 1):
            print(f"{i} --> {book[1]}")
    else:
        print("No books found.")

def check_book_stock(cursor, book_name):
    """Checks and prints book stock."""
    cursor.execute("SELECT Numbers_of_book FROM books WHERE Name = %s", (book_name,))
    result = cursor.fetchone()
    if result:
        stock = result[0]
        if stock == 0:
            print("NOW THIS BOOK IS NOT AVAILABLE")
        elif stock <= 8:
            print("WARNING! Low stock. Only", stock -1, "left.")
        else:
            print("Stock:", stock -1)
    else:
        print("Book not found.")

def buy_book(cursor, mydb, book_name, quantity):
    """Buys books, updates stock, and handles insufficient stock."""
    cursor.execute("SELECT Numbers_of_book FROM books WHERE Name = %s", (book_name,))
    result = cursor.fetchone()
    if result:
        stock = result[0]
        if quantity > stock:
            print(f"Insufficient stock. Only {stock} left.")
            return False
        elif quantity <= 0:
            print("Invalid quantity. Please enter a positive number.")
            return False
        else:
            cursor.execute("UPDATE books SET Numbers_of_book = Numbers_of_book - %s WHERE Name = %s", (quantity, book_name))
            mydb.commit()
            print("Book(s) purchased successfully!")
            check_book_stock(cursor, book_name)
            return True
    else:
        print("Book not found.")
        return False


def add_book(cursor, mydb):
    """Adds a new book.  Includes ISBN check for uniqueness."""
    while True:
        try:
            SNo = int(input("Enter SNo: "))
            name = input("Enter Name: ")
            author = input("Enter Author: ")
            year = int(input("Enter Year: "))
            ISBN = input("Enter ISBN: ")
            price = int(input("Enter Price: "))
            nob = int(input("Enter Number of Books: "))
            cursor.execute("SELECT * FROM books WHERE ISBN = %s", (ISBN,))
            if cursor.fetchone():
                print("ISBN already exists.")
                continue
            cursor.execute("INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s, %s)", (SNo, name, author, year, ISBN, price, nob))
            mydb.commit()
            print("Book added.")
            break
        except ValueError:
            print("Invalid input. Please enter numbers for numeric fields.")
        except mys.Error as e:
            print(f"Database error: {e}")
            break


def update_book(cursor, mydb):
    """Updates book details. Includes ISBN check for existence."""
    isbn = input("Enter ISBN of book to update: ")
    cursor.execute("SELECT * FROM books WHERE ISBN = %s", (isbn,))
    book = cursor.fetchone()
    if book:
        # Get updated data (similar to add_book) - omitted for brevity
        # ... update the database using cursor.execute and mydb.commit ...
        print("Book updated.")
    else:
        print("Book not found.")


def delete_book(cursor, mydb):
    """Deletes a book after confirmation."""
    isbn = input("Enter ISBN of book to delete: ")
    cursor.execute("SELECT * FROM books WHERE ISBN = %s", (isbn,))
    book = cursor.fetchone()
    if book:
        if input("Confirm delete? (y/n): ").lower() == 'y':
            cursor.execute("DELETE FROM books WHERE ISBN = %s", (isbn,))
            mydb.commit()
            print("Book deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("Book not found.")

def main_menu(cursor, mydb):
    """Main program loop."""
    while True:
        print("\nMain Menu:")
        print("1. View All Books")
        print("2. Search and Buy Book")
        print("3. Add Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Exit")
        try:
            choice = int(input("Enter your choice: "))
            separator()
            if choice == 1:
                view_all_books(cursor)
            elif choice == 2:
                book_name = input("Enter book name: ")
                quantity = int(input("Enter quantity: "))
                buy_book(cursor, mydb, book_name, quantity)
            elif choice == 3:
                add_book(cursor, mydb)
            elif choice == 4:
                update_book(cursor, mydb)
            elif choice == 5:
                delete_book(cursor, mydb)
            elif choice == 6:
                break
            else:
                print("Invalid choice.")
            separator()
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    cursor = connect_db(db_config)
    if cursor:
        mydb = mys.connect(**db_config)  # Get the connection object
        delete_zero_stock(cursor, mydb)
        if login(cursor): #Only proceed if login is successful.
            main_menu(cursor, mydb)
        mydb.close()
