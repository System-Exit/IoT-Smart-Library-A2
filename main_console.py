import library_user
import hashlib
import local_database
import os
import re
import sys
import socket
import json
import facial_recognition
from socket_utils import SocketUtils
sys.path.append("..")

LOCAL_DB_NAME = "library_user_database.db"
CONFIG_FILE_NAME = "config.json"


class ReceptionConsole:
    """
    Class for handling user information and user login
    for connecting to the 'Master Pi'
    """

    def __init__(self):
        # Check if config file is present and load it
        if os.path.isfile(CONFIG_FILE_NAME):
            with open(CONFIG_FILE_NAME, "r") as file:
                data = json.load(file)
        else:
            print("'%s' is required to run console." % CONFIG_FILE_NAME)
            sys.exit(1)
        # Specifies the address to connect to
        self.__address = (data["MasterPi_IP"], int(data["MasterPi_Port"]))
        # Initializes facial recognition
        self.__fc = facial_recognition.FacialRecognition()

    def display_console(self):
        """
        Displays the console and presents the user options to login/register
        """
        exit_program = False

        while exit_program is False:
            # Clears the terminal to clean screen

            print("*** Library Menu ***".center(32, ' '))
            print('{0: <31}'.format('Register New User'), '1')
            print('{0: <31}'.format('Register Face Recognition'), '2')
            print('{0: <31}'.format('Login with Credentials'), '3')
            print('{0: <31}'.format('Login with Face Recognition'), '4')
            print('{0: <31}'.format('Shutdown'), '0')

            selection = input("Select an option: ")

            if selection is '1':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.new_user_details()

            elif selection is '2':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.register_user_face()

            elif selection is '3':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.credential_login()

            elif selection is '4':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.face_login()

            elif selection is '0':
                os.system('cls' if os.name is 'nt' else 'clear')
                exit_program = True

            else:
                print("Invalid selection: Please try again!")

    def password_encryption(self, password):
        password = password.encode()
        hash_value = hashlib.sha256(password)
        hash_password = hash_value.hexdigest()
        return(hash_password)

    def new_user_details(self):
        """
        Prompt user for information including their first name, last name
        and email, then allow them to set a username and password for
        creating a new account.

        """
        first_name = input("Please Enter Your First Name: ").capitalize()
        last_name = input("Please Enter Your Last Name: ").capitalize()

        # Email must be passed through regex
        while True:
            email = input("Please Enter Your Email: ")
            if(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
                break
            else:
                print("Email not valid: Please try again...")

        # Must scan database to ensure username is unique
        username = input("Please Enter Desired Username: ")

        # Password must be hashed for encryption
        password = input("Please Enter Your Password: ")
        password = self.password_encryption(password)

        # Information must be stored in the database
        db = local_database.LocalDatabase(LOCAL_DB_NAME)

        if db.insert_new_user(first_name, last_name, email,
                              username, password) is 1:
            print("Username Already Exists, Please Try Another")

        elif db.insert_new_user(first_name, last_name, email,
                                username, password) is 2:
            print("Email Already Exists")

        else:
            print("Congratulations", first_name,
                  "you are now registered in our system!")

    def register_user_face(self):
        """
        Prompt user for their username and allow them
        To register their face for facial recognition
        based logins.

        """
        # Ask user for their username
        username = input("Please Enter Your Username: ")

        # Check in database that user exists
        db = local_database.LocalDatabase(LOCAL_DB_NAME)
        if not db.check_user_exists(username):
            print("User not found, have you registered yet?")
            return

        # Start face recognition process
        self.__fc.register_user(username)

    def credential_login(self):
        """
        Prompt user for their login details, scan database for
        username, compare hashed password.

        """
        username = input("Please Enter Your Username: ")
        password = input("Please Enter Your Password: ")
        password = self.password_encryption(password)

        db = local_database.LocalDatabase(LOCAL_DB_NAME)

        user = db.verify_login(username, password)
        if user is not False:
            self.send_request(user)
        else:
            print("Username/Password incorrect: Please Try Again")

    def face_login(self):
        """
        Allow user to login via facial recognition if they have
        registered their face for facial recognition.

        """
        # Begin facial recognition and get username of user
        username = self.__fc.recognize_user()
        # Check if user was not recognized
        if username is None:
            print("Your face could not be recognized.")
            print("Have you registered for face recognition?")
            return
        # Get user information
        db = local_database.LocalDatabase(LOCAL_DB_NAME)
        user = db.get_user_info(username)
        # Send request to master pi
        self.send_request(user)

    def send_request(self, user):
        """
        Sends login request and user details to master pi

        Args:
            user: Dictionary of user details

        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(self.__address))
            s.connect(self.__address)
            print("Successfully Connected")

            print("Logging in as {}".format(user["username"]))
            SocketUtils.sendJson(s, user)

            print("Waiting for Master Pi...")
            while(True):
                object = SocketUtils.recvJson(s)
                if("logout" in object):
                    print("Master Pi logged out.")
                    print()
                    break

# Starts the Reception Pi
if __name__ == "__main__":
    reception_console = ReceptionConsole()
    reception_console.display_console()
