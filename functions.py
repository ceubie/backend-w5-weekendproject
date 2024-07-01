from connect_to_sql import connect_db
import mysql.connector
from mysql.connector import Error
from datetime import date



# SQL interfacing functions
# #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Create
# ~~~~~~~~~

def add_book():

    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()

            bookname = input("What is the name of the book? ").title()
            genre = input("What is the genre of the book? ").title()
            authorname = input("What is the name of the author? ").title()
        
            cursor.execute("SELECT id FROM author WHERE name = (%s);", (authorname,))
            author = cursor.fetchone()

            if author is None:
                cursor.execute("INSERT INTO author (name) VALUES (%s);", (authorname,))
                conn.commit()
                author_id = cursor.lastrowid
                
            else:
                author_id = author[0]

            cursor.execute(
                "INSERT INTO books (name, genre, author_id) VALUES (%s, %s, %s);",
                (bookname, genre, author_id)
            ) 
            conn.commit()
            print("Book successfully added!")
        
        except Error as e:
            print(f"Error = {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


def add_user():

    conn = connect_db()
    if conn is not None:
        try:
            cursor = conn.cursor()

            libraryid = input("Please enter a 5 digit pin that you will remember. ")
            name = input("What is your name? ").title()
            phone = input("What is your phone number? ") 
            address = input("What is your address? ")
            email = input("What is your email? ")

            cursor.execute(
                "INSERT INTO users (library_id, name, phone, address, email) VALUES (%s, %s, %s, %s, %s);",
                (libraryid, name, phone, address, email)
            )           
            conn.commit()
            print("User successfully added!")


        except Error as e:
            print(f"Error = {e}") 

        finally:
            cursor.close()
            conn.close()

# Create
# ~~~~~~~~~


# - - - - - - - - - - - - - - 


# Update
# ~~~~~~~~~


def update_borrow_books():
    conn = connect_db()

    if conn is not None:
        try:
            cursor = conn.cursor()

            while True:
                option = input("Would you like to borrow a book, return a book, or quit? Select - b/r/q - ")

                if option == "q":
                    break

                elif option == "r":
                    try:
                        bookname = input("What book would you like to return? ").title()
                        username = input("What is your name? ").title()

                        cursor.execute("SELECT id FROM users WHERE name = %s;", (username,))
                        userid = cursor.fetchone()
                        if userid:
                            userid = userid[0]
                        else:
                            print("User not found.")
                            continue

                        cursor.execute("SELECT id FROM books WHERE name = %s;", (bookname,))
                        bookid = cursor.fetchone()
                        if bookid:
                            bookid = bookid[0]
                        else:
                            print("Book not found.")
                            continue

                        cursor.execute(
                            "UPDATE books SET availability = %s WHERE id = %s;", (1, bookid)
                        )

                        cursor.execute(                                                                               #~~~~~~~~
                            "DELETE FROM borrowed_books WHERE users_id = %s AND books_id = %s;", (userid, bookid)     # Delete                                                                                                                      #~~~~~~~~
                        )                                                                                             #~~~~~~~~

                        conn.commit()
                        print("Successfully returned book!")

                    except Error as e:
                        print(f"Error: {e}")
                        

                elif option == "b":
                    try:
                        bookname = input("What book would you like to borrow? ").title()
                        authorname = input("What is the name of the author? ").title()
                        username = input("What is your name? ").title()
                        today = date.today()

                        cursor.execute("SELECT id FROM books WHERE name = %s;", (bookname,))
                        bookid = cursor.fetchone()
                        if bookid:
                            bookid = bookid[0]
                        else:
                            print("Book not found.")
                            continue

                        cursor.execute("SELECT id FROM author WHERE name = %s;", (authorname,))
                        authorid = cursor.fetchone()
                        if authorid:
                            authorid = authorid[0]
                        else:
                            print("Author not found.")
                            continue

                        cursor.execute("SELECT id FROM users WHERE name = %s;", (username,))
                        userid = cursor.fetchone()
                        if userid:
                            userid = userid[0]
                        else:
                            print("User not found.")
                            continue

                        cursor.execute(
                            "UPDATE books SET availability = %s WHERE id = %s AND author_id = %s;", (0, bookid, authorid)
                        )

                        cursor.execute(
                            "INSERT INTO borrowed_books (users_id, books_id, borrow_date) VALUES (%s, %s, %s);",
                            (userid, bookid, today)
                        )

                        conn.commit()
                        print("Successfully borrowed book!")

                    except Error as e:
                        print(f"Error: {e}")
                        

        finally:
            cursor.close()
            conn.close()
                    
                

# Update
# ~~~~~~~~~



# - - - - - - - - - - - - - - 



# Retrieve
# ~~~~~~~~~~~


def display_all_books():
    conn = connect_db()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books;")

            for id, name, genre, availability, author_id in cursor.fetchall():
                print(f"{id}: {name} | {availability} | {genre} | {author_id}")

        except Error as e:
            print(f"Error = {e}")
        finally:
            cursor.close()
            conn.close()


def display_all_users():
    conn = connect_db()

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users;")

            results = cursor.fetchall()
            for result in results:
                print(result)
                

        except Error as e:
            print(f"Error = {e}")
        finally:
            cursor.close()
            conn.close()



def display_book():
    conn = connect_db()

    if conn is not None:
        try:
            cursor = conn.cursor()
            bookname = input("What is the name of the book? ")
            authorname = input("What is the name of the author? ")

            cursor.execute("SELECT id FROM author WHERE name = %s;", (authorname,))  #Finding author_id based off name
            authorid = cursor.fetchone()
            if authorid:
                authorid = authorid[0]
            else:
                print("Author not found.")
            
            cursor.execute("SELECT * FROM books WHERE name = %s AND author_id = %s;", (bookname, authorid))
            results = cursor.fetchall()
            print(results[0])

        except Error as e:
            print(f"Error = {e}")

        finally:
            cursor.close()
            conn.close()


def display_user():
    conn = connect_db()

    if conn is not None:
        try:
            cursor = conn.cursor()
            username = input("What is the name of the user? ")
            email = input("What is the email address? ")
            
            cursor.execute("SELECT * FROM users WHERE name = %s AND email = %s;", (username, email))
            results = cursor.fetchall()
            print(results)

        except Error as e:
            print(f"Error = {e}")

        finally:
            cursor.close()
            conn.close()

# Retrieve
# ~~~~~~~~~~~


# #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def book_operations():

    while True:
        option = input("""

     ---------Book Operations----------
                       
            1. Add a new book 
            2. Borrow/Return a book 
            3. Search for a book
            4. Display all books
            5. Go Back
                       
     ---------Select A Number----------

""")
        
        if option == "5":
            break
        elif option == "4":
            display_all_books()
        elif option == "3":
            display_book()
        elif option == "2":
            update_borrow_books()
        elif option == "1":
            add_book()



def user_operations():

    while True:
        option = input("""

     ---------User Operations----------
                       
            1. Add a new user
            2. View user details
            3. Display all users
            4. Go Back
                       
     ---------Select A Number----------

""")
        
        if option == "4":
            break
        elif option == "3":
            display_all_users()
        elif option == "2":
            display_user()
        elif option == "1":
            add_user()

