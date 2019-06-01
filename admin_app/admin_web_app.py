from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from app.flask_api import api, db
#from app import site

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Update HOST and PASSWORD appropriately.
HOST = '35.244.115.76'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'Library'

#URL to connect to:
# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>

INSTANCE_NAME = 'coral-silicon-242307:australia-southeast1:masterpi'


SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@{host}/{database}'
    '?unix_socket=/cloudsql/{instance_name}').format(
        user=USER, password=PASSWORD, host = HOST, 
        database=DATABASE, instance_name=INSTANCE_NAME
    )

# database_path = "mysql+pymysql://{}:{}@/{}?unix_socket=/cloudsql/{}".format(USER, PASSWORD, DATABASE, INSTANCE_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

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