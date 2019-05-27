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

```bash
$ python3 -m env env
```

Activate the virtual environment via:

```bash
$ source venv/bin/activate
```

While the virtual environment is activated, install the following via pip:
  
```bash
> pip3 install <flask>
> pip3 install <flask_wtf>
```

  In order to run the web app, while in the admin_app directory, type `flask run`. The home page can be accessed via the address shown, while
  the server is active, the server can be shutdown by typing `ctrl-c`.

In order to deactivate the virtual environment:

```bash
$ deactivate
```

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


## Voice Recognition

Voice Recognition for the smart library is used to search for books either by title or author. The project uses Google Speech-to-text with the default API for testing purposes. Rather than constantly streaming for voice input, the voice is invoked when needed (such as searching for a book by title or authoer), where the microphone will power on. The microphone adjusts for ambient noise, so it's important to give it a short second to adjust the threshold, before speaking into the microphone.

Google Speech Recognition will convert your speech to text, which will appear as a message on screen before automatically searching the the library's Google Database for a matchin result.

As we are using the Raspberry Pi for this prototype, we will need advanced access to the various cards and devices on our system, specifically the input (microphone) and output (speaker or headset in the 3.5mm jack on the Raspberry Pi).

The following website has been used to help set up the `.asroundrc` file which should be placed in `/home/pi`:

[https://developers.google.com/assistant/sdk/guides/service/python/embed/audio](https://developers.google.com/assistant/sdk/guides/service/python/embed/audio)