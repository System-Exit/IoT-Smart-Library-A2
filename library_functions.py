import datetime

class LibraryFunctions:
    def search_menu(self):


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
        # TODO Go Back option (go back to previous menu)

        # Get option from user
        opt = None
        while(opt is None):
            opt = input("Select an option: ")
            if(opt == "1"):
                # Have user enter title to search by
                title = input("Enter partial or full book title: ")
                query += "Title LIKE %%%s%%"
                values = [title]
            elif(opt == "2"):
                # Have user enter author to search by
                author = input("Enter partial or full author name: ")
                query += "Author LIKE %%%s%%"
                values = [author]
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
                query += "PublishedDate BETWEEN \
                          CAST(%s AS DATE) AND \
                          CAST(%s AS DATE)"
                values = [date_range_low, date_range_high]
            elif(opt == "4"):
                # Have user enter book ID to search by
                book_id = input("Enter ID of book: ")
                query += "BookID = %s"
                values = [book_id]
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        results = self.__gdb.search_books(query, values)
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

    def borrow_books(self, userID):
        """
        Asks user for the id of the book they wish to borrow,
        creates a borrow event in database and creates a
        calendar event for the borrowed book.

        Args:
            username (str): Username of the user borrowing the book

        """
        # Ask the user for the ID of the book they would like to borrow
        bookID = input("Enter the ID of book you would like to borrow: ")
        # Check that a book with that ID exists
        if(self.__gdb.check_book_exists(bookID)):
            # Inform the user that the book does not exist
            print("Book with given ID does not exist.")
        else:
            # Check if the book has been borrowed and not yet returned
            borrowed, book_borrowed_ID = self.__gdb.check_book_borrowed(bookID)
            if(borrowed):
                # Inform the user the book has already been borrowed
                print("This book has already been borrowed.")
            else:
                # Insert borrow entry into database and get its ID
                book_borrowed_ID = self.__gdb.create_borrow_entry(userID)
                # Create borrow event in calendar
                self.__gc.add_borrow_event(book_borrowed_ID, bookID, username)

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


        """
        # Ask the user for the ID of the book they are returning
        bookID = print("Enter the ID of the book you are returning: ")
        # Check that a book with that ID exists
        if(self.__gdb.check_book_exists(bookID)):
            # Inform the user that the book does not exist
            print("Book with given ID does not exist.")
        else:
            # Check if the book has been borrowed and not yet returned
            borrowed, book_borrowed_ID = self.__gdb.check_book_borrowed(bookID)
            if(borrowed):
                # Update the borrowed book database entry status
                self.__gdb.return_borrow_entry(book_borrowed_ID)
            else:
                # Inform the user this book has not been borrowed
                print("This book is not currently borrowed.")

        # Ask the user if they would like to return another book
        while True:
            response = input("Would you like to return another book?(Y/N): ")
            if(response.upper() == "Y"):
                # Recursively calls return books again
                self.return_books()
                return
            elif(response.upper() == "N"):
                return
            else:
                print("Invalid option.")

    @staticmethod
    def valid_date(date):
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