from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from config import Config

site = Blueprint("site", __name__)

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
# Client webpage. # Landing Page of website

@site.route("/login")
def index():
    
    #response = requests.get("http://127.0.0.1:5000/")
    # data = json.loads(response.text)

    return render_template("index.html")
    