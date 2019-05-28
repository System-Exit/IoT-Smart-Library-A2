from flask import render_template, redirect, request, url_for
from app import app
from app.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
#from app import site
db = SQLAlchemy(app)

#Contains all the routes for the application split into methods

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password"

    return render_template('login.html', title='Sign in', form=form, error=error)

@app.route('/books')
def books():
    
    books = None
    books = Book.query.all()

    return render_template("books.html", books = books)
