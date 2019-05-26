from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app

api = Blueprint("api", __name__)

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
    # Username = db.Column(db.String(256), unique = True)

    def __init__(self, BookID, Title, Author, PublisherDate):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublisherDate = PublisherDate

class PersonSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PubisherDate")

bookSchema = PersonSchema()
bookSchema = PersonSchema(many = True)

# Endpoint to show all books.
@api.route("/book", methods = ["GET"])
def getBooks():
    book = Book.query.all()
    result = bookSchema.dump(people)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/book/<id>", methods = ["GET"])
def getBook(id):
    person = Book.query.get(id)

    return bookSchema.jsonify(person)

# Endpoint to create new book.
@api.route("/book", methods = ["POST"])
def addBook():

    bookID = request.json["bookID"]
    Title = request.json[]
    Author = request.json[]
    PublisherDate = request.json[]

    newBook = Person(BookID = bookID, Title = Title, Author = Author, PublisherDate = PublisherDate)

    db.session.add(newBook)
    db.session.commit()

    return personSchema.jsonify(newPerson)

#---
# Up to here  : update for book
#--
# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person)