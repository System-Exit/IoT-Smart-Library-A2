import speech_recognition as sr
import google_api
import datetime
import subprocess

MIC_NAME = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"

class VoiceRecognition:
    def __init__(self):
        self.__gdb = google_api.GoogleDatabaseAPI()

    # Code by Matthew Bolger
    def voice_search(self):
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

            print("Say something for the Library!")
            try:
                audio = r.listen(source, timeout = 0.5)
            except sr.WaitTimeoutError:
                print("Listening timed out whilst waiting for phrase to start")
                return ""

        # recognize speech using Google Speech Recognition
        search_string = ""
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said '{}'".format(r.recognize_google(audio)))
            search_string = r.recognize_google(audio)
            return search_string
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


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
                self.voice_search()
                author = self.voice_search()
                clause += "Author LIKE %s"
                values = ["%"+author+"%"]
            else:
                print("Invalid option.")
                opt = None

        # Query the books database for all books that satisfy conditions
        print("Search the GDB")
        results = self.__gdb.search_books(clause, values)
        if results is not None:
            # Build formatting rules
            id_width = max(max(len(str(x[0])) for x in results),
                           len("ID"))
            title_width = max(max(len(str(x[1])) for x in results),
                              len("Title"))
            author_width = max(max(len(str(x[2])) for x in results),
                               len("Author"))
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
                                       str(book[3]).center(pub_date_width)))
        else:
            print("No books were found with this filter.")
