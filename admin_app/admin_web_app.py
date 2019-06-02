from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
import sqlalchemy, pymysql
from app.flask_api import api, db
#from app import site


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

# Update HOST and PASSWORD appropriately.
HOST = '35.244.115.76'
USER = 'root'
PASSWORD = 'root'
DATABASE = 'Library'

#URL to connect to:
# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>

INSTANCE_NAME = 'coral-silicon-242307:australia-southeast1:masterpi'

#{host}
# {host}
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@{host}/{database}'
    '?unix_socket=/cloudsql/{instance_name}').format(
        user=USER, password=PASSWORD, host=HOST, 
        database=DATABASE, instance_name=INSTANCE_NAME
    )

print(SQLALCHEMY_DATABASE_URI)



# database_path = "mysql+pymysql://{}:{}@/{}?unix_socket=/cloudsql/{}".format(USER, PASSWORD, DATABASE, INSTANCE_NAME)
# 'mysql+pymysql://root:root@35.244.115.76/Library?unix_socket=/cloudsql/coral-silicon-242307:australia-southeast1:masterpi'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(api)
#app.register_blueprint(site)

# Database information for Daniels Cloud SQL
# HOST = "35.244.106.216"
# USER = "masterpi"
# PASSWORD = "ipretsam"
# DATABASE = "Library"
# database_path = "mysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE)


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

#class BookSchema(ma.Schema):
#    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
#    def __init__(self, strict = True, **kwargs):
#        super().__init__(strict = strict, **kwargs)
#    
#    class Meta:
#        # Fields to expose.
#        fields = ("BookID", "Title", "Author", "PubisherDate")

#bookSchema = BookSchema()
#bookSchema = BookSchema(many = True)

if __name__ == "__main__":
    app.run(host = "0.0.0.0")