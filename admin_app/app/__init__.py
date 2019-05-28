from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from config import Config

#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')

app = Flask(__name__)
app.config.from_object(Config)

from app import routes


@app.route("/")
def home():
    
    #response = requests.get("http://127.0.0.1:5000/")
    # data = json.loads(response.text)

    return render_template("home.html")