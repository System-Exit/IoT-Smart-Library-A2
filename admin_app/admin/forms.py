from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

# Create a form to interact with the database

class EditBookForm(FlaskForm):
    BookID = StringField('Book ID', validators=[DataRequired()])
    Title = StringField('Title', validators=[DataRequired()])
    Author = StringField('Author', validators=[DataRequired()])
    PublishedDate = DateField('Published Date', validators=[DataRequired()])
    ISBN = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Submit')
