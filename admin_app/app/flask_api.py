from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app

api = Blueprint("api", __name__) #TODO Check what this does

app = Flask(__name__)

db = SQLAlchemy(app)
ma = Marshmallow()

#Change all these API calls to reflect our book table

# Declaring the model.
class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text, nullable = False)
    Author = db.Column(db.text, nullable = False)
    PublisherDate = db.cloumn(db.date, nullable = False)    

    def __init__(self, BookID, Title, Author, PublisherDate):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublisherDate = PublisherDate

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PubisherDate")

bookSchema = BookSchema()
bookSchema = BookSchema(many = True)

# Endpoint to show all books.
@api.route("/book", methods = ["GET"])
def getBooks():
    book = Book.query.all()
    result = bookSchema.dump(book)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/book/<id>", methods = ["GET"])
def getBook(id):
    person = Book.query.get(id)

    return bookSchema.jsonify(person)

# Endpoint to create new book.
@api.route("/book", methods = ["POST"])
def addBook():

    bookID = request.json["BookID"]
    Title = request.json["Title"]
    Author = request.json["Author"]
    PublisherDate = request.json["PublisherDate"]

    newBook = Book(BookID = bookID, Title = Title, Author = Author, PublisherDate = PublisherDate)

    db.session.add(newBook)
    db.session.commit()

    return bookSchema.jsonify(newBook)


# Endpoint to update person.
@api.route("/book/<id>", methods = ["PUT"])
def bookUpdate(id):
    book = Book.query.get(id)
    title = request.json["name"]

    book.Title = title

    db.session.commit()

    return bookSchema.jsonify(book)

# Endpoint to delete person.
@api.route("/book/<id>", methods = ["DELETE"])
def bookDelete(id):
    book = Book.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return bookSchema.jsonify(person)