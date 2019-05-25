## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
## and Matthew Bolger (PIoT S1 2019)

from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

class QRScanner:
    """
    Class for handling QR code detection.

    """

    def __init__(self):
        """
        Constructor for QR code detection.

        Should accept arg for path or link for QR codes.

        """
        pass

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
            
            # wait a little before scanning again
            time.sleep(1)

        # Stop the video stream
        print("[INFO] closing video stream...")
        vs.stop()
        print(barcodeData)
        return barcodeData


    def __init_video_stream(self):
        print("[INFO] starting video stream...")
        vs = VideoStream( src = -1 ).start()
        time.sleep(2.0)
        return vs
        

# for testing, delete
if __name__ == "__main__":
    qr = QRScanner()
    qr.read_barcode()
    