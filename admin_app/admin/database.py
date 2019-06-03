from flask import Flask, Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from flask import current_app as app


db = SQLAlchemy()
ma = Marshmallow()

def create_app(app):
    
    #HOST = '35.244.115.76'
    #USER = 'root'
    #PASSWORD = 'root'
    #DATABASE = 'Library'

    # Database information for Daniels Cloud SQL
    HOST = "35.244.106.216"
    USER = "masterpi"
    PASSWORD = "ipretsam"
    DATABASE = "Library"
    # database_path = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE)
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False) 
    
    db.init_app(app)
    ma.init_app(app)

# Declaring the model.
class Book(db.Model):
    __tablename__ = "Book"
    BookID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Title = db.Column(db.Text, nullable = False)
    Author = db.Column(db.Text, nullable = False)
    PublishedDate = db.Column(db.Date, nullable = False)    
    ISBN = db.Column(db.Text, nullable=False)

    def __init__(self, BookID, Title, Author, PublishedDate, ISBN):
        self.BookID = BookID
        self.Title = Title
        self.Author = Author
        self.PublishedDate = PublishedDate
        self.ISBN = ISBN

class BookSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(strict = strict, **kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("BookID", "Title", "Author", "PubishedDate", "ISBN")

bookSchema = BookSchema()
bookSchema = BookSchema(many = True)
