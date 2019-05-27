# COSC2674 Programming Internet of Things - Assignment 2

## Group members
| Name | Student number |
|--|:--:|
| Yianna Phaedonos | `s3615301` |
| Tom Plowman | `s3604589` |
| James Laine-wyllie | `s3607269` |
| Daniel Linford | `s3661720` |

---
## Overview
### About this project

*This project has been designed for use with two Raspberry Pi Model B+'s (a reception pi and a master pi) and a webcam (project uses Microsoft® LifeCam HD-3000).*

This prototype is designed to automate a Library Management System (LMS) for two types of users: **library user** and **library admin**. 

#### Library User Features
* Register with the library, via text
* Registered users can register for face recognition
* Log into the LMS, via text or face recognition
* Search, Borrow and Return a book

#### Library Admin Features
* Flask web application
* Add or remove books
* Generate visual reports

The project also uses OpenCV for facial recognition and object detection, and a cloud-based database using Google Cloud Platform (GCP), which both need to be installed on the Master Pi. These are lengthy processes, so please allow some time for setup.


## Facial Recognition

Facial reognition required 3 stages: building the image dataset, encoding the images in the dataset and recognition of new images.

Once users are registered, they can opt to register for facial recognition. The user needs to press enter on the keyboard to take photos, and the system will notify them if an image has been captured or if no face has been detected.

*It is recommended that a dataset of 30 photos with natural and unnatural facial expressions are recorded before encoding.*


## Main Console (Reception Pi)

The main console runs on the first Raspberry Pi and is a command line interface (CLI), which acts as the initial entry for the LMS. User details are stored and passwords are encrypted in a local database. Once a user logs into the system, the Master Pi (LMS) is sent the user's username via sockets. Unsuccessful login attempt does not allow the user passed this system.


## Master Console (Master Pi)

Once the Master Pi receives confirmation via sockets, the LMS displays a CLI. Main functionality of the LMS is displayed here, including searching for a book via voice or QR code.


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

**Our implementation of this feature can be unreliable. Make sure the ambient noise level is very low and that you talk directly into the microphone.**

Voice Recognition for the smart library is used to search for books either by title or author. The project uses Google Speech-to-text with the default API for testing purposes. 

To get Voice Recognition to work in our Smart Library, the following packages need to be installed:

```bash
$ pip3 install SpeechRecognition
$ sudo apt-get install portaudio10-dev python-all-dev python3-all-dev
$ pip3 install pyaudio
$ pip3 install google-api-python-client
$ sudo apt-get install flac
```

Rather than constantly streaming for voice input, the speech-to-text recognizer is invoked when needed (such as searching for a book by title or author). The microphone powers on, and adjusts for ambient noise. It's important to **wait a second before speaking** so it adjusts its ambient noise threshold accurately.

As this project uses the Raspberry Pi for this prototype, you will need advanced access to the various cards and devices on your system, specifically the input (microphone) and output (speaker or headset in the 3.5mm jack on the Raspberry Pi).

The following website has been used to help set up the `.asroundrc` file which should be placed in `/home/pi`. Ensure you run through the test recording and playback.

[https://developers.google.com/assistant/sdk/guides/service/python/embed/audio](https://developers.google.com/assistant/sdk/guides/service/python/embed/audio)




