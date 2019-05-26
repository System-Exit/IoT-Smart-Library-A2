import MySQLdb
import json
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleDatabaseAPI:
    """"
    Class for handling API calls to the Google cloud database

    """
    def __init__(self):
        """
        Constructor for google database API.
        Reads config file for database details.

        """
        # Load config file to get database details
        with open("gdb_config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            host = config["host"]
            user = config["user"]
            password = config["password"]
            database = config["database"]

        # Create connection to database
        self.__connection = MySQLdb.connect(host, user, password, database)

    def get_userID_by_username(self, username):
        """
        Queries the database for a user by the given name and gets their ID

        Args:
            username (str): Username of the user to get ID of

        Returns:
            The ID of the given user if they exits, None otherwise.

        """
        # Define insert statement
        query = "SELECT UserID FROM User WHERE UserName = %s"
        parameters = (username,)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
        # Return the ID if the user exists, None otherwise
        if result is None:
            return None
        else:
            return result[0]

    def add_user(self, username, first_name, last_name):
        """
        Adds a new user to the database with given username and name

        Args:
            username (str): Username of the user
            first_name (str): First name of the user
            last_name (str): Last name of the user

        Returns:
            The ID of the newly added user

        """
        # Define query
        query = "INSERT INTO User (UserName, FName, LName) VALUES (%s, %s, %s)"
        parameters = (username, first_name, last_name)
        # Create user in user table
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            userID = cursor.lastrowid
        # Commit changes
        self.__connection.commit()
        # Return the ID of the new user
        return userID

    def search_books(self, clause=None, parameters=None):
        """
        Search the books table with given WHERE clause and parameters and
        returns the result.

        Args:
            clause (:obj: `str`, optional): WHERE clause in SQL syntax that
                the clause will use. Default is none.
            parameters (:obj:`tuple` of :obj:`str`, optional):
                The parameters of a parameterized query. Default is none.

        Returns:
            The results of the query as a list of tuples

        """
        # Define query
        if clause is None:
            query = "SELECT * FROM Book"
        else:
            query = "SELECT * FROM Book WHERE " + clause
        # Execute query and return result
        with self.__connection.cursor() as cursor:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            return cursor.fetchall()

    def create_borrow_entry(self, bookID, userID):
        """
        Create a borrow entry for a given book in database

        Args:
            bookID (str): ID of the book to create borrow entry for
            userID (str): ID of user that will be borrowing the book

        Returns:
            The generated ID for the book borrow entry

        """
        # Define insert statement
        query = "INSERT INTO BookBorrowed (UserID, BookID, Status, BorrowedDate) \
                 VALUES (%s, %s, 'borrowed', CURDATE())"
        parameters = (userID, bookID)
        # Create borrowed entry in book borrow table
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            book_borrow_ID = cursor.lastrowid
        # Commit changes
        self.__connection.commit()
        # Return the ID of the borrowed book
        return str(book_borrow_ID)

    def return_borrow_entry(self, book_borrowed_ID):
        """
        Update a borrow entry status field to "returned"

        Args:
            book_borrowed_ID (str): ID of borrow event to update

        """
        # Define update statement
        query = "UPDATE BookBorrowed SET Status = 'Returned' \
                 WHERE BookBorrowedID = %s"
        parameters = (book_borrowed_ID,)
        # Update borrowed entry in book borrow table
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
        # Commit changes
        self.__connection.commit()

    def check_book_exists(self, bookID):
        """
        Queries the database to check if the book with ID exists.

        Args:
            bookID (str): The ID of the book to check

        Returns:
            bool: True if book with ID exists, False otherwise.

        """
        # Define query
        query = "SELECT * FROM Book WHERE BookID = %s"
        parameters = (bookID,)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
        # Return whether or not the book exists
        if result is None or result[0] == "borrowed":
            return False
        else:
            return True

    def check_book_borrowed(self, bookID):
        """
        Queries the database to check if the book is currently borrowed.

        Args:
            bookID (str): The ID of the book to check

        Returns:
            True and BookBorrowedID if book is currently borrowed.
            False and None if book is not currently borrowed.

        """
        # Define query
        query = "SELECT BookBorrowedID FROM BookBorrowed WHERE BookID = %s \
                 AND Status = 'borrowed'"
        parameters = (bookID,)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
        # Return whether or not the book is currently borrowed
        if result is None:
            return False, None
        else:
            return True, result[0]


class GoogleCalendarAPI:
    """
    Class for handling operations with google calendar.

    """
    def __init__(self):
        """
        Constructor for google calendar API.
        Loads necessary configuration files for accessing a user's calendar.

        """
        # Load token for Google calendar API
        scope = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("gc_token.json")
        creds = store.get()
        # If token file does not exist or is invalid, run through API setup
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("gc_credentials.json", scope)
            creds = tools.run_flow(flow, store)
        # Builds API service
        self.__service = build("calendar", "v3", http=creds.authorize(Http()))

    def add_borrow_event(self, book_borrow_ID, bookID, username):
        """
        Adds a new borrow calendar event for a borrowed book.

        Args:
            book_borrow_ID (str): ID that will be inlcuded in event ID
            bookID (str): ID of the book that is being borrowed
            username (str): Username of the user borrowing the book

        """
        # Define return date of book seven days from now
        return_date = (datetime.datetime.now() + datetime.timedelta(days=7))
        # Create event with details of borrowing including book ID and user
        summary = "Book %s borrowed" % str(bookID)
        location = "RMIT PIoT Library"
        description = ("A book with an ID number of %s has "
                       "been borrowed by %s and is due to be returned "
                       "by this date.") % (str(bookID), str(username))
        eventID = "piotbb%s" % str(book_borrow_ID)
        event = {
            "id": eventID,
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "date": return_date.strftime("%Y-%m-%d"),
            },
            "end": {
                "date": return_date.strftime("%Y-%m-%d"),
            }
        }
        # Insert calendar event into calendar
        self.__service.events().insert(
            calendarId="primary", body=event).execute()

    def remove_borrow_event(self, book_borrowed_ID):
        """
        Removes an existing borrow calendar event for a book.

        Args:
            book_borrowed_ID (str): ID of the book borrow entry in GDB

        """
        # Generate event ID of calendar event for borrowed book
        eventID = "piotbb%s" % str(book_borrowed_ID)
        # Delete calendar event for borrowed book
        self.__service.events().delete(calendarId="primary",
                                       eventId=eventID).execute()
