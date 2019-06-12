from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlalchemy, pymysql
import os, requests, json
from admin.database import Book, bookSchema, db
#from flask import current_app as app

api = Blueprint("api", __name__) 


# Endpoint to show all books.
@api.route("/api/book", methods = ["GET"])
def getBooks():
    book = Book.query.all()
    result = bookSchema.dump(book)

    return jsonify(result.data)

# Endpoint to get book by id.
@api.route("/api/book/<int:id>", methods = ["GET"])
def getBook(id):
    book = Book.query.get(id)

    return bookSchema.jsonify(book)

# Endpoint to create new book.
@api.route("/api/book", methods = ["POST"])
def addBook():

    bookID = request.json["BookID"]
    Title = request.json["Title"]
    Author = request.json["Author"]
    PublishedDate = request.json["PublishedDate"]
    ISBN = request.json["ISBN"]

    newBook = Book(BookID = bookID, Title = Title, Author = Author, PublishedDate = PublishedDate, ISBN=ISBN)

    db.session.add(newBook)
    db.session.commit()

    return bookSchema.jsonify(newBook)


# Endpoint to update book.
@api.route("/api/book/<id>", methods = ["PUT"])
def bookUpdate(id):
    book = Book.query.get(id)
    title = request.json["name"]

    book.Title = title

    db.session.commit()

    return bookSchema.jsonify(book)

# Endpoint to delete book.
@api.route("/api/book/<id>", methods = ["DELETE"])
def bookDelete(id):
    book = Book.query.get(id)

    db.session.delete(book)
    db.session.commit()

    return bookSchema.jsonify(book)

