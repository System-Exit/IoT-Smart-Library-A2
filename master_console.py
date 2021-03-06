#!/usr/bin/env python3
import socket
import google_api
import datetime
import os
import sys
from socket_utils import SocketUtils
from qr_scanner import QRScanner


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
        # Initialize and bind socket to listen on
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("", listen_port))
        # Load google database API
        self.__gdb = google_api.GoogleDatabaseAPI()
        # Load google calendar API
        self.__gc = google_api.GoogleCalendarAPI()

    def connect_to_reception(self):
        """
        Waits for a connection to a reception pi and then waits until a
        username is sent where it will let the display_console method handle
        the user.

        """
        # Listen for reception pi
        self.__socket.listen()
        print("Waiting for Reception Pi to connect...")
        # Accept the connection from reception pi
        try:
            conn, addr = self.__socket.accept()
        # If the user presses ctrl-c while waiting for a connection,
        # close the socket and end the program gracefully
        except KeyboardInterrupt:
            print("Stopping Master Pi.")
            self.__socket.close()
            sys.exit()
        # Handle connection
        print("Reception PI has connected!")
        with conn:
            # Receive username and user's name
            data = SocketUtils.recvJson(conn)
            username = data["username"]
            first_name = data["firstname"]
            last_name = data["lastname"]
            # Add user details to database if this their first login
            userID = self.__gdb.get_userID_by_username(username)
            if not userID:
                self.__gdb.add_user(username, first_name, last_name)
            # Start console menu
            self.display_console(userID, username, first_name)
            # Send logoff message
            SocketUtils.sendJson(conn, {"logout": "true", })

    def keyboard_input(self):
        string = input("Enter search string: ")
        return string

    def display_console(self, userID, username, first_name):
        """
        Displays console menu and gets an option from user.

        Args:
            userID (str): User ID of the connected user.
            username (str): Username of the connected user.
            first_name (str): first name of the connected user.

        """
        while True:
            qr = QRScanner()
            # Welcome user and display menu
            os.system('cls' if os.name is 'nt' else 'clear')
            print(("Welcome %s!" % first_name).center(26, ' '))
            print("*** Library Menu ***".center(26, ' '))
            print("{0: <25}".format("Search for a book"), "1")
            print("{0: <25}".format("Borrow a book"), "2")
            print("{0: <25}".format("Return a book"), "3")
            print("{0: <25}".format("Search by voice"), "4")
            print("{0: <25}".format("Search by QR code"), "5")
            print("{0: <25}".format("Logout"), "0")

            # Get option from user
            opt = None
            while opt is None:
                opt = input("Select an option: ")
                # Handle option from user
                if opt == "1":
                    # Let user search for a book
                    self.search_books(opt, True, False, False)
                elif opt == "2":
                    # Let user borrow book
                    self.borrow_books(userID, username)
                elif opt == "3":
                    # Let user return book
                    self.return_books()
                # Voice UI
                elif opt == "4":
                    print("Sorry, this isn't working right now.")
                    opt = None
                    # recoqnizer.search_books()
                elif opt == "5":
                    # just call search books from qr function here
                    # get it working
                    string = qr.read_barcode()
                    qr.search_books(string)
                elif opt == "0":
                    # Logs off master pi console
                    return
                else:
                    print("Invalid option.")
                    opt = None

    def search_options(self, opt):
        # Display options for what field to search for books by
        if not opt == "5":
            print("What field would you like to search by?")
            print("1. Title")
            print("2. Author")
            if not opt == "4":
                print("3. Publication date")
                print("4. Book ID")
            print("0. Back")

    def search_books(self, opt, text=False, voice=False, qr=False):
        """
        Asks user to specify a property and property value, which
        is then used in a search of all books in the database and
        the result is formatted and displayed to the user.

        Args:
            text (bool): Whether or not to search by text. Default false.
            voice (bool): Whether or not to search by voice. Default false.
            qr (bool): Whether or not to serach by QR code. Default false.

        """
        # Initialize clause for search
        clause = ""
        self.search_options(opt)
        # Get option from user
        opt = None
        while opt is None:
            opt = input("Select an option: ")
            if opt == "1":
                # Have user enter title to search by
                if text is True:
                    title = input("Enter partial or full book name: ")
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
                if text is True:
                    book_id = input("Enter ID of book: ")
                elif voice is True:
                    book_id = qr.read_barcode()
                clause += "BookID = %s"
                values = [book_id]
            # Go to previous menu if user accidentally made wrong selection
            elif opt == "0":
                return
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        results = self.__gdb.search_books(clause, values)
        if results:
            # Build formatting rules
            id_width = max(max(len(str(x[0])) for x in results),
                           len("ID"))
            title_width = max(max(len(str(x[1])) for x in results),
                              len("Title"))
            author_width = max(max(len(str(x[2])) for x in results),
                               len("Author"))
            pub_date_width = len("Publish Date")
            isbn_width = max(13, len("ISBN"))
            total_width = sum((id_width, title_width, author_width,
                               pub_date_width, isbn_width, 4))
            # Display all options on screen
            print("%s|%s|%s|%s|%s" % ("ID".center(id_width),
                                      "Title".center(title_width),
                                      "Author".center(author_width),
                                      "Publish Date".center(pub_date_width),
                                      "ISBN".center(isbn_width)))
            print('-'*total_width)
            for book in results:
                print("%s|%s|%s|%s|%s" % (str(book[0]).rjust(id_width),
                                          str(book[1]).ljust(title_width),
                                          str(book[2]).ljust(author_width),
                                          str(book[3]).center(pub_date_width),
                                          str(book[4]).center(isbn_width)))
        else:
            print("No books were found with this filter.")
        # Wait for user to press enter before returning to menu
        input("Press enter to return to menu.")

    def borrow_books(self, userID, username):
        """
        Asks user for the id of the book they wish to borrow,
        creates a borrow event in database and creates a
        calendar event for the borrowed book.

        Args:
            userID (str): ID of the user borrowing the book.
            username (str): Username of the user borrowing the book.

        """
        # Ask the user for the ID of the book they would like to borrow
        qr = QRScanner()
        print("{0: <25}".format("Search by ID"), "1")
        print("{0: <25}".format("Search by QR code"), "2")
        print("{0: <25}".format("Go back"), "0")

        # Ask the user for the ID of the book they are returning
        opt = None
        while opt is None:
            opt = input("Select an option: ")
            # Handle option from user
            if opt == "1":
                # User enters ID of book
                bookID = input("Enter the ID of book you ",
                               "would like to borrow: ")
            elif opt == "2":
                # User scans QR code
                bookID = qr.read_barcode()
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
                self.borrow_books(userID, username)
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
        qr = QRScanner()
        print("{0: <25}".format("Search by ID"), "1")
        print("{0: <25}".format("Search by QR code"), "2")
        print("{0: <25}".format("Go back"), "0")

        # Ask the user for the ID of the book they are returning
        opt = None
        while opt is None:
            opt = input("Select an option: ")
            # Handle option from user
            if opt == "1":
                # User enters ID of book
                bookID = input("Enter the ID of the book you are returning: ")
            elif opt == "2":
                # User scans QR code
                bookID = qr.read_barcode()

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
                # Update calendar by removing borrow calendar event
                self.__gc.remove_borrow_event(book_borrowed_ID)
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
            bool: Whether or not the date is valid.

        """
        try:
            # Split date into year, month and day
            year, month, day = date.split("-")
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
    while True:
        master_console.connect_to_reception()
