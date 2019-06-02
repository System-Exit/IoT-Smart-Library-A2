from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from admin.database import create_app
from admin.flask_api import api
import admin.routes
from config import Config

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

#from flask import Flask, Blueprint, request, jsonify, render_template, session, abort
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#from forms import LoginForm
#import os, requests, json
#from config import Config
#from admin import app
#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')



@app.route("/")
def index():
    
  #  if not session.get('logged_in'):
  #    return render_template("login.html")
  #  else:
  #    return render_template("home.html")
    
  #  return render_template("home.html")
  return "hi"

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
