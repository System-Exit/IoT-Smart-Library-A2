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

In order to run the web app locally sveral dependendencies are required:
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