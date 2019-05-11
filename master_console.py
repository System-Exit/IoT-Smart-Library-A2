import socket

class MasterConsole:
    """
    Class for handling all user interaction with the pi.

    """
    
    def __init__(self, port = 65000):
        """
        Constructor for master console.

        Args:
            port (int, optional): The port the application will listen on. 
                Defaults to 65000. 

        """
        self.port = port

    def connect_to_reception(self):
        """
        Waits for a connection to a reception pi and then waits until a username is
        sent where it will let the display_console method handle the user

        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Bind socket to listen on specified port
            sock.bind(("", self.port))
            sock.listen()

            # Accept the connection from reception pi
            conn, addr = sock.accept()
            with conn:
                # Continuously loop getting username from reception, handling
                # the user then sending a logoff message
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
        # Display menu
        print("Hello %s" % user_name)
        print("Select an option:")
        print("1. Search a book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("0. Logout")

        # Get option from user
        opt = input("Select an option: ")

        # Handle option from user
        if(opt == "1"):
            # Let user search for a book
            self.search_books()
        elif(opt == "2"):
            # Let user borrow book
            self.borrow_books()
        elif(opt == "3"):
            # Let user return book
            self.return_books()
        elif(opt == "0"):
            return
        else:
            print("Invalid option.")

    def search_books(self):
        """
        Asks user to specify how they want to search 
        for a book then displays the books that match
        given criteria.

        TODO

        """
        pass

    def borrow_books(self):
        """
        Asks user for the id of the book they wish to borrow, 
        creates a borrow event in database and creates a 
        calendar event for the borrowed book.

        TODO

        """
        pass

    def return_books(self):
        """
        Asks user for the ID of the book they wish to return, 
        updates the corresponding borrow database entry and 
        deletes the corresponding calendar event.

        TODO

        """
        pass

# Starts the Master Pi Console
if __name__ == "__main__":
    master_console = MasterConsole()
    master_console.connect_to_reception()
