from flask import Flask, request, jsonify, render_template, url_for, redirect
from admin.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from admin.database import create_app
from admin.flask_api import api
#import admin.routes
from admin.config import Config

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


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', title='Sign in', form=form, error=error)

@app.route('/books')
def books():
    
    books = None
    try:
        books = Book.query.all()
    except Exception as e:
            print("Failed to get books")
            print(e)
    
    return render_template("books.html", books = books)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = EditBookForm()
    books = None

    try:
        books = Book.query.all()
    except Exception as e:
            print("Failed to get books")
            print(e)

    return render_template("edit.html", books = books, form=form)


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
