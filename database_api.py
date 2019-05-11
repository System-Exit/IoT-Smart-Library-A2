import MySQLdb
import json


class GoogleDatabaseAPI:
    def __init__(self):
        """
        Constructor for google database API
        Reads config file for database details

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
        if(clause is None):
            query = "SELECT * FROM BOOKS"
        else:
            query = "SELECT * FROM Books WHERE " + clause
        # Execute query and return result
        with self.__connection.cursor() as cursor:
            if(parameters is None):
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            return cursor.fetchall()

    def create_borrow_event(self, bookID, userID):
        """
        Create a borrow entry for a given book in database

        Args:
            bookID (str): ID of the book to create borrow entry for
            userID (str): ID of user that will be borrowing the book

        """
        # Define insert statement
        query = "INSERT INTO BookBorrow (LmsUserID, BookID, Status, BorrowedDate) \
                 VALUES (%s, %s, \"borrowed\", CURDATE())"
        parameters = (userID, bookID)
        # Create borrowed entry in book borrow table
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
        # Commit changes
        self.__connection.commit()

    def get_userID(user_name):
        """
        Queries and returns the ID of the user by their name

        Args:
            user_name (str): The username of the user

        Returns:
            str: ID of the given user

        """
        # Define query
        query = "SELECT LmsUserID FROM LmsUser WHERE UserName = %s"
        parameters = (user_name)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchone()[0]

    def check_book_exists(self, bookID):
        """
        Queries the database to check if the book with ID exists.

        Args:
            bookID (str): The ID of the book to check

        Returns:
            bool: True if book with ID exists, False otherwise.

        """
        # Define query
        query = "SELECT * FROM Books WHERE BookID = %s"
        parameters = (bookID)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
        # Return whether or not the book exists
        if(result is None or result[0] == "borrowed"):
            return False
        else:
            return True

    def check_book_available(self, bookID):
        """
        Queries the database to check if the book is not currently borrowed.

        Args:
            bookID (str): The ID of the book to check

        Returns:
            bool: True if book is not borrowed, False if book is borrowed.

        """
        # Define query
        query = "SELECT Status FROM BookBorrowed WHERE BookID = %s AND BookBorrowedID in \
            (SELECT MAX(BookBorrowedID) FROM BookBorrowed GROUP BY BookID)"
        parameters = (bookID)
        # Execute query and get result
        with self.__connection.cursor() as cursor:
            cursor.execute(query, parameters)
            result = cursor.fetchone()
        # Return whether or not the book is currently borrowed
        if(result is None or result[0] == "borrowed"):
            return False
        else:
            return True