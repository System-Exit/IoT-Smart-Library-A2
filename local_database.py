import sqlite3

class LocalDatabase:
    def __init__(self, name):
        self.name = name
    
    #Inserts the new user details into the database, after verifying that 'username' and 'email' are unique
    def insert_new_user(self, first_name, last_name, email, username, password):
        connection = sqlite3.connect(self.name)

        with connection:
            cursor = connection.cursor()

            row = cursor.execute(
                """SELECT COUNT(*) FROM users
                WHERE (username = :username)""", {"username": username}
            )

            for row in cursor:
                count_result = row[0]

            #Username is unique
            if count_result is 0:
                row = cursor.execute(
                    """SELECT COUNT(*) FROM users
                    WHERE (email = :email)""", {"email": email}
                )
                
                for row in cursor:
                    count_result = row[0]
                
                #Email is unique
                if count_result is 0:
                    connection.execute(
                        """INSERT INTO users (f_name, l_name, email, username, password)
                        VALUES (:f_name, :l_name, :email, :username, :password)""", 
                        {"f_name": first_name, "l_name": last_name, "email": email, "username": username, "password": password}
                    )
                    connection.commit()

                #Email already exists in database
                else:
                    return 2

            #Username already exists in database
            else:
                return 1
        connection.close()

    #Returns True if username and password match, False otherwise
    def verify_login(self, username, password):
        connection = sqlite3.connect(self.name)

        with connection:
            cursor = connection.cursor()

            row = cursor.execute(
                """SELECT COUNT(*) FROM users
                WHERE (username = :username) AND (password = :password)""", {"username": username, "password": password}
            )

            for row in cursor:
                count_result = row[0]

            #A match has been found, login details have been confirmed
            if count_result is 1:
                return True
            
            else:
                return False
        connection.close()
