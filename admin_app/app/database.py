from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app


app = Flask(__name__)
db = SQLAlchemy(app)



# Declaring the model.
class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text, nullable = False)
    Author = db.Column(db.Text, nullable = False)
    PublisherDate = db.Column(db.Date, nullable = False)    
    # field for isbn
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