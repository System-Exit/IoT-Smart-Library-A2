import library_user
import hashlib
import local_database
import os
import re
import sys
import socket
import json
from socket_utils import SocketUtils
sys.path.append("..")

LOCAL_DB_NAME = "library_user_database"

with open("config.json", "r") as file:
    data = json.load(file)

HOSTNAME = data["MasterPi_IP"]
PORT = 65000
ADDRESS = (HOSTNAME, PORT)


class ReceptionConsole:
    """
    Class for handling user information and user login
    for connecting to the 'Master Pi'
    """

    def __init__(self, send_port=65000):
        # Specifies the port to send to
        self.__send_port = send_port

    def display_console(self):
        """
        Displays the console and presents the user options to login/register
        """
        exit_program = False

        while exit_program is False:
            # Clears the terminal to clean screen

            menu_str = "*** Library Menu ***"
            print(menu_str.center(26, ' '))
            self.library_menu()

            selection = input("Select an option: ")

            if selection is '1':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.new_user_details()

            elif selection is '2':
                os.system('cls' if os.name is 'nt' else 'clear')
                self.existing_user_login()

            elif selection is '3':
                os.system('cls' if os.name is 'nt' else 'clear')
                exit_program = True

            else:
                print("Invalid selection: Please try again!")

    def library_menu(self):
        print('{0: <25}'.format('Register New User'), '1')
        print('{0: <25}'.format('Login'), '2')
        print('{0: <25}'.format('Shutdown'), '3')

    def password_encryption(self, password):
        password = password.encode()
        hash_value = hashlib.sha256(password)
        hash_password = hash_value.hexdigest()
        return(hash_password)

    def new_user_details(self):
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

    # Prompt user for their login details, scan database for
    # username, compare hashed password
    def existing_user_login(self):
            username = input("Please Enter Your Username: ")
            password = input("Please Enter Your Password: ")
            password = self.password_encryption(password)

            db = local_database.LocalDatabase(LOCAL_DB_NAME)

            user = db.verify_login(username, password)
            if user is not False:
                self.send_request(user)
            else:
                print("Username/Password incorrect: Please Try Again")

    def send_request(self, user):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Connecting to {}...".format(ADDRESS))
            s.connect(ADDRESS)
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
