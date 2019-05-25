#!/usr/bin/env python3

import socket
import google_api
import datetime
import socket_utils
from voice_ui import VoiceRecognition


class MasterConsole:
    """
    Class for handling all user interaction with the pi.

    """

    def __init__(self, listen_port=65000):
        """
        Constructor for master console.

        Args:
            listen_port (int, optional): The port the application will
                listen on. Defaults to 65000.

        """
        # Specify port to listen on
        self.__listen_port = listen_port
        # Load google database API
        self.__gdb = google_api.GoogleDatabaseAPI()
        # Load google calendar API
        self.__gc = google_api.GoogleCalendarAPI()

    def connect_to_reception(self):
        """
        Waits for a connection to a reception pi and then waits until a
        username is sent where it will let the display_console method handle
        the user

        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Bind socket to listen on specified port
            sock.bind(("", self.__listen_port))
            sock.listen()

            # Accept the connection from reception pi
            print("Waiting for Reception Pi to connect...")
            conn, addr = sock.accept()
            print("Reception PI has connected!")
            with conn:
                # Continuously loop getting user info from reception, handling
                # the user then sending a logoff message once user logs off
                while True:
                    print("Waiting for user to connect...")
                    # Receive username and user's name
                    data = socket_utils.recvJson(conn)
                    username = data["username"]
                    first_name = data["firstname"]
                    last_name = data["lastname"]
                    # Add user details to database if this their first login
                    userID = self.__gdb.get_userID_by_username(username)
                    if not userID:
                        self.__gdb.add_user(username, first_name, last_name)
                    # Display console
                    self.display_console(userID, username, first_name)
                    # Send logoff message
                    socket_utils.sendJson(conn, {"logout": "true", })

    def display_console(self, userID, username, name):
        """
        Displays console menu and gets an option from user.

        Args:
            username (str): Username of the connected user.

        """
        while True:
            recoqnizer = VoiceRecognition()

            # Display menu
            print("Hello %s" % name)
            print("Select an option:")
            print("1. Search a book")
            print("2. Borrow a book")
            print("3. Return a book")
            # Voice UI
            print("4. Voice Search a book")
            print("0. Logout")

            # Get option from user
            opt = None
            while opt is None:
                opt = input("Select an option: ")
                # Handle option from user
                if opt == "1":
                    # Let user search for a book
                    self.search_books()
                elif opt == "2":
                    # Let user borrow book
                    self.borrow_books(userID, username)
                elif opt == "3":
                    # Let user return book
                    self.return_books()
                # Voice UI
                elif opt == "4":
                    recoqnizer.search_books()
                elif opt == "0":
                    # Logs off master pi console
                    return
                else:
                    print("Invalid option.")
                    opt = None

    def search_books(self):
        """
        Asks user to specify a property and property value, which
        is then used in a search of all books in the database and
        the result is formatted and displayed to the user

        """
        # Initialize clause for search
        clause = ""
        # Display options for what field to search for books by
        print("What field would you like to search by?")
        print("1. Title")
        print("2. Author")
        print("3. Publication date")
        print("4. Book ID")
        # Get option from user
        opt = None
        while opt is None:
            opt = input("Select an option: ")
            if opt == "1":
                # Have user enter title to search by
                title = input("Enter partial or full book title: ")
                clause += "Title LIKE %s"
                values = ["%"+title+"%"]
            elif opt == "2":
                # Have user enter author to search by
                author = input("Enter partial or full author name: ")
                clause += "Author LIKE %s"
                values = ["%"+author+"%"]
            elif opt == "3":
                # Have user enter date range to search by
                valid_input = False
                while not valid_input:
                    date_range_low = input(
                        "Enter publication date low range(yyyy-mm-dd): ")
                    if(self.valid_date(date_range_low)):
                        valid_input = True
                    else:
                        print("Date is invalid.")
                valid_input = False
                while not valid_input:
                    date_range_high = input(
                        "Enter publication date high range(yyyy-mm-dd): ")
                    if(self.valid_date(date_range_high)):
                        valid_input = True
                    else:
                        print("Date is invalid.")
                clause += "PublishedDate BETWEEN \
                          CAST(%s AS DATE) AND \
                          CAST(%s AS DATE)"
                values = [date_range_low, date_range_high]
            elif opt == "4":
                # Have user enter book ID to search by
                book_id = input("Enter ID of book: ")
                clause += "BookID = %s"
                values = [book_id]
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        results = self.__gdb.search_books(clause, values)
        if results is not None:
            # Build formatting rules
            id_width = max(max(len(str(x[0])) for x in results),
                           len("ID"))
            title_width = max(max(len(str(x[1])) for x in results),
                              len("Title"))
            author_width = max(max(len(str(x[2])) for x in results),
                               len("Author"))
            pub_date_width = len("Publish Date")
            total_width = id_width+title_width+author_width+pub_date_width+3
            # Display all options on screen
            print("%s|%s|%s|%s" % ("ID".center(id_width),
                                   "Title".center(title_width),
                                   "Author".center(author_width),
                                   "Publish Date".center(pub_date_width)))
            print('-'*total_width)
            for book in results:
                print("%s|%s|%s|%s" % (str(book[0]).rjust(id_width),
                                       str(book[1]).ljust(title_width),
                                       str(book[2]).ljust(author_width),
                                       str(book[3]).center(pub_date_width)))
        else:
            print("No books were found with this filter.")

    def borrow_books(self, userID, username):
        """
        Asks user for the id of the book they wish to borrow,
        creates a borrow event in database and creates a
        calendar event for the borrowed book.

        Args:
            userID (str): ID of the user borrowing the book
            username (str): Username of the user borrowing the book

        """
        # Ask the user for the ID of the book they would like to borrow
        bookID = input("Enter the ID of book you would like to borrow: ")
        # Check that a book with that ID exists
        if not self.__gdb.check_book_exists(bookID):
            # Inform the user that the book does not exist
            print("Book with given ID does not exist.")
        else:
            # Check if the book has been borrowed and not yet returned
            borrowed, book_borrowed_ID = self.__gdb.check_book_borrowed(bookID)
            if borrowed:
                # Inform the user the book has already been borrowed
                print("This book has already been borrowed.")
            else:
                # Insert borrow entry into database and get its ID
                book_borrowed_ID = self.__gdb.create_borrow_entry(
                    bookID, userID)
                # Create borrow event in calendar
                self.__gc.add_borrow_event(book_borrowed_ID, bookID, username)

        # Ask the user if they would like to borrow another book
        while True:
            response = input("Would you like to borrow another book?(Y/N): ")
            if response.upper() == "Y":
                # Recursively calls borrow books again
                self.borrow_books()
                return
            elif response.upper() == "N":
                return
            else:
                print("Invalid option.")

    def return_books(self):
        """
        Asks user for the ID of the book they wish to return,
        updates the corresponding borrow database entry and
        deletes the corresponding calendar event.


        """
        # Ask the user for the ID of the book they are returning
        bookID = input("Enter the ID of the book you are returning: ")
        # Check that a book with that ID exists
        if not self.__gdb.check_book_exists(bookID):
            # Inform the user that the book does not exist
            print("Book with given ID does not exist.")
        else:
            # Check if the book has been borrowed and not yet returned
            borrowed, book_borrowed_ID = self.__gdb.check_book_borrowed(bookID)
            if borrowed:
                # Update the borrowed book database entry status
                self.__gdb.return_borrow_entry(book_borrowed_ID)
            else:
                # Inform the user this book has not been borrowed
                print("This book is not currently borrowed.")

        # Ask the user if they would like to return another book
        while True:
            response = input("Would you like to return another book?(Y/N): ")
            if response.upper() == "Y":
                # Recursively calls return books again
                self.return_books()
                return
            elif response.upper() == "N":
                return
            else:
                print("Invalid option.")

    def valid_date(self, date):
        """
        Checks if given date is valid and returns true if so, false if not.

        Args:
            date (str): String of date in the format of YYYY-MM-DD.

        Returns:
            Whether or not the date is valid.

        """
        # Split date into year, month and day
        year, month, day = date.split("-")
        try:
            # Attempt to parse the date
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            # Parse failed, so return false
            return False
        # Parse was successful, so return true
        return True

# Starts the Master Pi Console
if __name__ == "__main__":
    master_console = MasterConsole()
    master_console.connect_to_reception()
