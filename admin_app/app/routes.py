from flask import render_template
from app import app
from app.forms import LoginForm

#Contains all the routes for the application split into methods

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        
        if(request.form['username'] == "jaqen" and request.form['password'] == "hghar"):
            return redirect('/index')
        else:
            error = "Invalid username or password"

    return render_template('login.html', title='Sign in', form=form, error=error)
