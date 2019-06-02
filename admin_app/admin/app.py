from flask import Flask, request, jsonify, render_template, routes
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from flask_api import api, db
from config import Config
from database import create_app
#from app import site


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)

create_app(app)


app.register_blueprint(api)
#app.register_blueprint(site)

# Database information for Daniels Cloud SQL
# HOST = "35.244.106.216"
# USER = "masterpi"
# PASSWORD = "ipretsam"
# DATABASE = "Library"
# database_path = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")