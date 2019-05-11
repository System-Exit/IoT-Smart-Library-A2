import socket
import database_api
import datetime


class MasterConsole:
    """
    Class for handling all user interaction with the pi.

    """

    def __init__(self, listen_port):
        """
        Constructor for master console.

        Args:
            listen_port (int, optional): The port the application will
                listen on. Defaults to 65000.

        """
        # Specify port to lisetn on
        self.__listen_port = listen_port
        # Load google database api
        self.__gdb = database_api.GoogleDatabaseAPI()

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
            conn, addr = sock.accept()
            with conn:
                # Continuously loop getting username from reception, handling
                # the user then sending a logoff message once user logs off
                while True:
                    print("Waiting for user to connect...")
                    user_name = conn.recv(4096).decode()
                    self.display_console(user_name)
                    conn.sendall("logoff".encode())

    def display_console(self, user_name):
        """
        Displays console menu and gets an option from user.


        Args:
            user_name (str): Username of the connected user.

        """
        while True:
            # Display menu
            print("Hello %s" % user_name)
            print("Select an option:")
            print("1. Search a book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("0. Logout")

            # Get option from user
            opt = None
            while(opt is None):
                opt = input("Select an option: ")
                # Handle option from user
                if(opt == "1"):
                    # Let user search for a book
                    self.search_books()
                elif(opt == "2"):
                    # Let user borrow book
                    self.borrow_books(user_name)
                elif(opt == "3"):
                    # Let user return book
                    self.return_books()
                elif(opt == "0"):
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
        # Initialize query for search
        query = "SELECT * FROM Book WHERE "
        # Display options for what field to search for books by
        print("What field would you like to search by?")
        print("1. Title")
        print("2. Author")
        print("3. Publication date")
        print("4. Book ID")
        print("5. Begin search!")
        # Get option from user
        opt = None
        while(opt is None):
            opt = input("Select an option: ")
            if(opt == "1"):
                # Have user enter title to search by
                title = input("Enter partial or full book title: ")
                clause += "Title LIKE %%%s%%"
                values = (title)
            elif(opt == "2"):
                # Have user enter author to search by
                author = input("Enter partial or full author name: ")
                clause += "Author LIKE %%%s%%"
                values = (author)
            elif(opt == "3"):
                # Have user enter date range to search by
                valid_input = False
                while not valid_input:
                    date_range_low = input(
                        "Enter publication date low range(yyyy-mm-dd): ")
                    if(valid_date(date_range_low)):
                        valid_input = True
                    else:
                        print("Date is invalid.")
                valid_input = False
                while not valid_input:
                    date_range_high = input(
                        "Enter publication date high range(yyyy-mm-dd): ")
                    if(not valid_date(date_range_high)):
                        valid_input = True
                    else:
                        print("Date is invalid.")
                clause += "PublishedDate BETWEEN \
                          CAST(%s AS DATE) AND \
                          CAST(%s AS DATE)"
                values = (date_range_low, date_range_high)
            elif(opt == "4"):
                # Have user enter book ID to search by
                book_id = input("Enter ID of book: ")
                clause += "BookID = %s"
                values = (book_id)
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        results = self.__gdb.search_books(clause, values)
        if(results is not None):
            # Build formatting rules
            id_width = max(max(len(x[0]) for x in results), len("ID"))
            title_width = max(max(len(x[1]) for x in results), len("Title"))
            author_width = max(max(len(x[2]) for x in results), len("Author"))
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
                                       str(book[3]).center()))
        else:
            print("No books were found with this filter.")

    def borrow_books(self, user_name):
        """
        Asks user for the id of the book they wish to borrow,
        creates a borrow event in database and creates a
        calendar event for the borrowed book.

        Args:
            user_name (str): Username of the user borrowing the book

        TODO: Add calendar event creation

        """
        # Ask the user for the ID of the book they would like to borrow
        id = input("Enter the ID of book you would like to borrow: ")
        # Check that a book with that ID exists
        if(self.__gdb.check_book_exists(id)):
            # Inform the user that the book does not exist
            print("Book with given ID does not exist.")
        else:
            # Check if the book has been borrowed and not yet returned
            if(self.__gdb.check_book_available(id)):
                # Inform the user the book has already been borrowed
                print("This book has already been borrowed.")
            else:
                # Get user id of user
                userID = self.__gdb.get_userID(user_name)
                # Insert borrow event into database
                self.__gdb.create_borrow_event(userID)
                # Create borrow event in calendar TODO
                pass

        # Ask the user if they would like to borrow another book
        while True:
            response = input("Would you like to borrow another book?(Y/N): ")
            if(response.upper() == "Y"):
                # Recursively calls borrow books again
                self.borrow_books()
                return
            elif(response.upper() == "N"):
                return
            else:
                print("Invalid option.")

    def return_books(self):
        """
        Asks user for the ID of the book they wish to return,
        updates the corresponding borrow database entry and
        deletes the corresponding calendar event.

        TODO

        """
        pass

    @staticmethod
    def valid_date(date)
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
