# COSC2674 Programming Internet of Things - Assignment 2

## Group members
| Name | Student number |
|--|:--:|
| Yianna Phaedonos | `s3615301` |
| Tom Plowman | `s3604589` |
| James Laine-wyllie | `s3607269` |
| Daniel Linford | `s3661720` |

---
## Webapp

In order to run the web app locally, several dependendencies are required:
  * flask
  * flask_wtf

We will run a virtual environment to keep these packages seperate from our
global environment

  * $ python3 -m env env

Activate the virtual environment via:

  * $ source venv/bin/activate

While the virtual environment is activated:
  
  Installed via pip
    
    * $ pip3 install <flask>
    * $ pip3 install <flask_wtf>

  In order to run the web app, in the admin_app directory:

    * $ flask run 

  The home page can be accessed via the address shown, while
  the server is active:

    * The server can be shutdown via ctrl-c

In order to deactivate the virtual environment:

    * $ deactivate


## Object Detection for QR Codes

As books usually have a barcode, we have incorporated a QR code reading features. The QR codes hold a unique number, which is associated with a specific copy of a book in the library system. This allows individual books to be distinguished, for example, in cases such as vandalism and repairs to binding.

OpenCV has been used for the object detection, but to distinguish and read 2 dimensional QR codes, we need to install Pyzbar.

```bash
$ pip3 install pyzbar
```

As the QR codes are being compared directly to the Unique ID, this is the basic information required for the reader. A scanned QR code will return a string, which is passed to a method that searches our Google Database directly. 

### Search a book

An extra option is present in the main menu, so that the QR reader can scan a code and bring up the relevant search results.

### Return a book

An extra option is present to allow a user to return a book by scanning the QR code.