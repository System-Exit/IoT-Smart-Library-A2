from flask import render_template, redirect, request, url_for, session, abort, Blueprint
from admin.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
import json, requests
#from app import site
# db = SQLAlchemy(app)
site = Blueprint("site", __name__)
#Contains all the routes for the application split into methods

@site.route('/')
@site.route('/index')
def index():
    #USE API endpoints
    
    #response = requests.get("http://127.0.0.1:5000/api/book")
    #data = json.loads(response.text)

    return render_template("index.html")

@site.route('/login')
def login():

    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            return render_template('index.html')
        else:
            error = "Invalid username or password"

    return render_template('login.html', title='Sign in', form=form, error=error)

@site.route('/books', methods=['GET'])
def books():
  
  form = EditBookForm()
  
  #Call api endpoint to query database
  response = requests.get("http://127.0.0.1:5000/api/book")
  data = json.loads(response.text)


  return render_template(books.html, books=data, form=form)

@site.route('/books', methods=['POST'])
def add():
  
  form = EditBookForm()
  #Take data from from, post via api endpoint
  bookID = form.BookID.data
  Title = form.Title.data
  Author = form.Author.data
  PublishedDate = form.PublishedDate.data
  ISBN = form.ISBN.data

  data = {
        "BookID": bookID,
        "Title": Title,
        "Author": Author,
        "PublishedDate": PublishedDate,
        "ISBN": ISBN
        
    }

  headers = {
        "Content-type": "application/json"
    }

  response = requests.post("http://127.0.0.1:5000/api/book", data=json.dumps(data), headers=headers)
  data = json.loads(response.text)

  return redirect("/books")

@site.route('/delete')
def delete():

  #Get Title of book to delete
  bookID = request.form['bookID'] 
  # Use REST API.
  response = requests.delete("http://127.0.0.1:5000/api/book/" + bookID)
  data = json.loads(response.text)

  return redirect("/")
