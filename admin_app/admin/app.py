from flask import Flask, request, jsonify, render_template, url_for, redirect
from admin.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from admin.database import create_app, Book, bookSchema, db
from admin.flask_api import api
#import admin.routes
from admin.config import Config

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)

create_app(app)


app.register_blueprint(api)
#app.register_blueprint(site)

#from flask import Flask, Blueprint, request, jsonify, render_template, session, abort
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#from forms import LoginForm
#import os, requests, json
#from config import Config
#from admin import app
#site = Blueprint("site", __name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            return render_template('index.html')
        else:
            error = "Invalid username or password"

    return render_template('login.html', title='Sign in', form=form, error=error)

@app.route('/books', methods=['GET', 'POST'])
def books():
    
    form = EditBookForm()
    books = None

    if request.method == 'GET':
        
        try:
                books = Book.query.all()
        except Exception as e:
                print("Failed to get books")
                print(e)
        
        return render_template("books.html", books = books, form=form)

    elif request.method == 'POST' and form.vaidate():

        bookID = form.BookID.data
        Title = form.Title.data
        Author = form.Author.data
        PublishedDate = form.PublishedDate.data
        ISBN = form.ISBN.data

        newBook = Book(BookID = bookID, Title = Title, Author = Author, PublishedDate = PublishedDate, ISBN=ISBN)

        db.session.add(newBook)
        db.session.commit()

        return render_template("books.html", books = books, form=form)  

# Endpoint to get book by id.
@app.route("/book/<int:id>", methods = ["GET"])
def getBook(id):
    book = Book.query.get(id)

    return bookSchema.jsonify(book)

#@app.route("/book", methods = ['POST'])
#def addBook():
#
#    form = EditBookForm()
#    
#    if request.method == 'POST' and form.vaidate():
#                
#
#       bookID = form.BookID.data
#        Title = form.Title.data
#        Author = form.Author.data
#        PublishedDate = form.PublishedDate.data
#        ISBN = form.ISBN.data
#
#        newBook = Book(BookID = bookID, Title = Title, Author = Author, PublishedDate = PublishedDate, ISBN=ISBN)
#
#        db.session.add(newBook)
#        db.session.commit()
#
#        return bookSchema.jsonify(newBook)

#@app.route('/book', methods=["GET"])
#def edit():
#    form = EditBookForm()
#   books = None
#
#    try:
#        books = Book.query.all()
#    except Exception as e:
#            print("Failed to get books")
#            print(e)
#
#    return render_template("edit.html", books = books, form=form)

@app.route("/book/<id>", methods = ["DELETE"])
def bookDelete(id):

    try:
            
        book = Book.query.get(id)

        db.session.delete(book)
        db.session.commit()

        return bookSchema.jsonify(book)
    except:
        print("error")

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
