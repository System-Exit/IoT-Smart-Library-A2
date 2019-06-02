from flask import render_template, redirect, request, url_for, session, abort
from admin.forms import LoginForm, EditBookForm
from flask_sqlalchemy import SQLAlchemy
import app
#from app import site
# db = SQLAlchemy(app)

#Contains all the routes for the application split into methods


