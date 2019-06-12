from flask import Flask, request, jsonify, render_template, url_for, redirect
from admin.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from admin.database import create_app, Book, bookSchema, db
from admin.flask_api import api
from admin.routes import site
from admin.config import Config

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)

create_app(app)


app.register_blueprint(api)
app.register_blueprint(site)

#from flask import Flask, Blueprint, request, jsonify, render_template, session, abort
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#from forms import LoginForm
#import os, requests, json
#from config import Config
#from admin import app
#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
