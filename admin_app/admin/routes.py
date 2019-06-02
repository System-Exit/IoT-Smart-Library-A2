from flask import render_template, redirect, request, url_for, session, abort
from app import app
from app.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
#from app import site
# db = SQLAlchemy(app)

#Contains all the routes for the application split into methods

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            session['logged_in'] = True
            return redirect(url_for('home'))
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
