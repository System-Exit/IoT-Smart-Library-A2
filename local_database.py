import sqlite3


class LocalDatabase:
    def __init__(self, name):
        self.name = name

    def insert_new_user(self, first_name, last_name,
                        email, username, password):
        """
        Inserts the new user details into the database
        after verifying that 'username' and 'email' are unique.

        Args:
            first_name (str): First name of user
            last_name (str): Last name of user
            email (str): Email of user
            username (str): Username of user
            password (str): Hashed password of user

        Returns:
            1 if user with username already exists
            2 id user with email already exists

        """
        connection = sqlite3.connect(self.name)
        connection.row_factory = sqlite3.Row

        with connection:
            cursor = connection.cursor()
            # Check username is unique
            row = cursor.execute(
                """SELECT COUNT(*) FROM users
                WHERE (username = :username)""", {"username": username}
            )
            count_result = cursor.fetchone()[0]
            # Return 1 if not unique
            if count_result is not 0:
                return 1

            # Check email is unique
            row = cursor.execute(
                """SELECT COUNT(*) FROM users
                WHERE (email = :email)""", {"email": email}
            )
            count_result = cursor.fetchone()[0]
            # Return 2 if not unique
            if count_result is not 0:
                return 2

            # Add user to database
            connection.execute(
                """
                INSERT INTO users
                (f_name, l_name, email, username, password)
                VALUES (:f_name, :l_name, :email, :username, :password)
                """,
                {"f_name": first_name, "l_name": last_name,
                    "email": email, "username": username,
                    "password": password}
            )
            connection.commit()
        connection.close()

    def verify_login(self, username, password):
        """
        Returns the user if the entered username and password is a match

        """
        connection = sqlite3.connect(self.name)
        connection.row_factory = sqlite3.Row

        with connection:
            cursor = connection.cursor()

            cursor.execute(
                """SELECT * FROM users
                WHERE (username = :username) AND (password = :password)""",
                {"username": username, "password": password}
            )

            row = cursor.fetchone()

        connection.close()

        if row is not None:
            return {"username": row["username"], "firstname": row["f_name"],
                    "lastname": row["l_name"], "email": row["email"]}
        else:
            return False

    def get_user_info(self, username):
        """
        Queries database for user information and dict including
        usrename, firstname, lastname, and email

        Args:
            username (str): Username of the user to get data of

        Returns:
            Dictionary object of all specified user data from database

        """
        connection = sqlite3.connect(self.name)
        connection.row_factory = sqlite3.Row

        # Query database for user info
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT * FROM users
                WHERE (username = :username)""", {"username": username}
            )
            row = cursor.fetchone()
        connection.close()

        # Return user info
        if row is not None:
            return {"username": row["username"], "firstname": row["f_name"],
                    "lastname": row["l_name"], "email": row["email"]}
        else:
            return None

    def check_user_exists(self, username):
        """
        Check if user exists in database or not.

        Args:
            username (str): Username of user to check for

        Retruns:
            True if user exists, False if user does not exist

        """
        connection = sqlite3.connect(self.name)
        connection.row_factory = sqlite3.Row

        # Search database for user
        with connection:
            cursor = connection.cursor()
            row = cursor.execute(
                """SELECT COUNT(*) FROM users
                WHERE (username = :username)""", {"username": username}
            )
            row = cursor.fetchone()
        connection.close()

        # Return whether or not a user exists
        count_result = row[0]
        return count_result is not 0
