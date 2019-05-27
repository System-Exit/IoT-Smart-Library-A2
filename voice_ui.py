# ACKNOWLEDGEMENT
# Code by Matthew Bolger adapted for this project

import speech_recognition as sr
import google_api
import datetime
import subprocess

MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"


class VoiceRecognition:
    def __init__(self):
        self.__gdb = google_api.GoogleDatabaseAPI()

    def voice_search(self):
        # To test searching without the microphone uncomment this line of code
        # return input("Enter the first name to search for: ")
        print("[INFO] Initialising voice search...")

        # Set the device ID of the mic that we specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if(microphone_name == MIC_NAME):
                device_id = i
                break

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone(device_index = device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source)

            print("Ask Library about the book...")
            try:
                audio = r.listen(source, timeout = 1.5)
            except sr.WaitTimeoutError:
                return None

        # recognize speech using Google Speech Recognition
        firstName = None
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("[INFO] Decoding audio ")
            firstName = r.recognize_google(audio)
        except(sr.UnknownValueError, sr.RequestError):
            pass
        finally:
            return firstName

    def search_books(self):
        """
        Asks user to specify a property and property value, which
        is then used in a search of all books in the database and
        the result is formatted and displayed to the user

        """
        # Initialize clause for search
        clause = ""
        # Display options for what field to search for books by
        print("What field would you like to search by?")
        print("1. Title")
        print("2. Author")
        print("0. Go back")
        # Get option from user
        opt = None
        while opt is None:
            opt = input("Select an option: ")
            if opt == "1":
                # Have user enter title to search by
                title = self.voice_search()
                clause += "Title LIKE %s"
                values = ["%"+title+"%"]
            elif opt == "2":
                # Have user enter author to search by
                author = self.voice_search()
                clause += "Author LIKE %s"
                values = ["%"+author+"%"]
            elif opt == "0":
                return
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        print("Search the GDB")
        results = self.__gdb.search_books(clause, values)
        if results:
            # Build formatting rules
            id_width = max(max(len(str(x[0])) for x in results),
                           len("ID"))
            title_width = max(max(len(str(x[1])) for x in results),
                              len("Title"))
            author_width = max(max(len(str(x[2])) for x in results),
                               len("Author"))
            pub_date_width = len("Publish Date")
            isbn_width = max(13, len("ISBN"))
            total_width = sum((id_width, title_width, author_width,
                               pub_date_width, isbn_width, 4))
            # Display all options on screen
            print("%s|%s|%s|%s|%s" % ("ID".center(id_width),
                                      "Title".center(title_width),
                                      "Author".center(author_width),
                                      "Publish Date".center(pub_date_width),
                                      "ISBN".center(isbn_width)))
            print('-'*total_width)
            for book in results:
                print("%s|%s|%s|%s|%s" % (str(book[0]).rjust(id_width),
                                          str(book[1]).ljust(title_width),
                                          str(book[2]).ljust(author_width),
                                          str(book[3]).center(pub_date_width),
                                          str(book[4]).center(isbn_width)))
        else:
            print("No books were found with this filter.")
        # Wait for user to press enter before returning to menu
        input("Press enter to return to menu.")
