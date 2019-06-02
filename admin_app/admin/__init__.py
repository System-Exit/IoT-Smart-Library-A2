from flask import Flask, Blueprint, request, jsonify, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import LoginForm
import os, requests, json
from config import Config
from admin import app
#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')


from admin import routes


@app.route("/")
def index():
    
  #  if not session.get('logged_in'):
  #    return render_template("login.html")
  #  else:
  #    return render_template("home.html")
    
    return render_template("home.html")

  