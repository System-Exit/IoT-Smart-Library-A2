import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or b',\x8f\xaeV\x03*?\xee\xf6JZ\xf6$r\xb1-'