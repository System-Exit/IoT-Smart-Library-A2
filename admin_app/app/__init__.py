from flask import Flask, Blueprint, request, jsonify, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from app.forms import LoginForm
import os, requests, json
from config import Config

#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')

app = Flask(__name__)
app.config.from_object(Config)

from app import routes


@app.route("/")
def home():
    
  #  if not session.get('logged_in'):
  #    return render_template("login.html")
  #  else:
  #    return render_template("home.html")
    
    return render_template("home.html")

  
