from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from app.flask_api import api, db
#from app import site

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Update HOST and PASSWORD appropriately.
HOST = "35.244.115.76"
USER = "default"
PASSWORD = "default"
DATABASE = "Library"

database_path = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)

app.register_blueprint(api)
#app.register_blueprint(site)

# Database information for Daniels Cloud SQL
#HOST = "35.244.106.216"
#USER = "masterpi"
#PASSWORD = "ipretsam"
#DATABASE = "Library"

if __name__ == "__main__":
    app.run(host = "0.0.0.0")