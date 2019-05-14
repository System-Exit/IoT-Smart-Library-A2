import library_user
import hashlib
import local_database
import os
import re

LOCAL_DB_NAME = "library_user_database"

def main():
    exit_program = False

    while exit_program is False:
        #Clears the terminal to clean screen

        menu_str = "*** Library Menu ***"
        print(menu_str.center(26, ' '))
        library_menu()

        selection = input("Select an option: ")

        if selection is '1':
            os.system('cls' if os.name is 'nt' else 'clear')
            new_user_details()

        elif selection is '2':
            os.system('cls' if os.name is 'nt' else 'clear')
            existing_user_login()

        elif selection is '3':
            os.system('cls' if os.name is 'nt' else 'clear')
            exit_program = True

        else:
            print("Invalid selection: Please try again!")
            

def library_menu():        
    print(f'{"Register New User":25} 1')
    print(f'{"Login":25} 2')
    print(f'{"Shutdown":25} 3')

def password_encryption(password):
    password = password.encode()
    hash_value = hashlib.sha256(password)
    hash_password = hash_value.hexdigest()
    return(hash_password)

def new_user_details():
    first_name = input("Please Enter Your First Name: ").capitalize()
    last_name = input("Please Enter Your Last Name: ").capitalize()

    #Email must be passed through regex
    while True:
        email = input("Please Enter Your Email: ")
        if(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            break
        else:
            print("Email not valid: Please try again...")

    #Must scan database to ensure username is unique
    username = input("Please Enter Desired Username: ")

    #Password must be hashed for encryption
    password = input("Please Enter Your Password: ")
    password = password_encryption(password)

    #Information must be stored in the database
    db = local_database.LocalDatabase(LOCAL_DB_NAME)
    
    if db.insert_new_user(first_name, last_name, email, username, password) is 1:
        print("Username Already Exists, Please Try Another")

    elif db.insert_new_user(first_name, last_name, email, username, password) is 2:
        print("Email Already Exists")

    else:
        print("Congratulations", first_name, "you are now registered in our system!")

#Prompt user for their login details, scan database for username, compare hashed password
def existing_user_login():
        username = input("Please Enter Your Username: ")
        password = input("Please Enter Your Password: ")
        password = password_encryption(password)

        db = local_database.LocalDatabase(LOCAL_DB_NAME)
        
        #Send login request to Master Pi
        if db.verify_login(username, password) is True:
            print("Login Successful")

        else:
            print("Username/Password incorrect: Please Try Again")

main()