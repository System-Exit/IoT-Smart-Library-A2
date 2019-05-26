## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
## and Matthew Bolger (PIoT S1 2019)

from imutils.video import VideoStream
from pyzbar import pyzbar
import google_api
import datetime
import imutils
import time
import cv2
import os
import sys

class QRScanner:
    """
    Class for handling QR code detection.

    """

    def __init__(self):
        """
        Constructor for QR code detection.

        Should accept arg for path or link for QR codes.

        """
        # Load google database API
        self.__gdb = google_api.GoogleDatabaseAPI()

    def read_barcode(self):
        print("[INFO] starting video stream...")
        vs = VideoStream( src = -1 ).start()
        time.sleep(2.0)

        found = set()
        barcodeData = ""

        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width = 400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

        # loop over the detected barcodes
        for barcode in barcodes:
            # the barcode data is a bytes object so we convert it to a string
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # if the barcode text has not been seen before print it and update the set
            if barcodeData not in found:
                print("[FOUND] Type: {}, Data: {}".format(barcodeType, barcodeData))
                found.add(barcodeData)          

        # Stop the video stream
        print("[INFO] closing video stream...")
        vs.stop()
        print(barcodeData)
        return barcodeData

    def search_books(self, string):
        """
        Asks user to specify a property and property value, which
        is then used in a search of all books in the database and
        the result is formatted and displayed to the user

        """
        # Initialize clause for search
        clause = ""

        # Get option from user

        # Have user enter book ID to search by
        book_id = string
        clause += "BookID = %s"
        values = [book_id]

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


    def __init_video_stream(self):
        print("[INFO] starting video stream...")
        vs = VideoStream( src = -1 ).start()
        time.sleep(2.0)
        return vs
    
    