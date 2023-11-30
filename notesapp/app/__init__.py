from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor #Initialization of flask-ckeditor
import os

app = Flask(__name__) # create Flask object 
ckeditor = CKEditor(app) # initialize chededitor 
basedir = os.path.abspath(os.path.dirname(__file__)) # get path where python script is located 

app.config.from_mapping( 
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'password', # secret key for security 
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False # disable sql tracking mods 
)


login = LoginManager(app) #initialize flask login 
login.login_view = 'login' # redirect 
db = SQLAlchemy(app) # db initlaization 
migrate = Migrate(app, db) # extension for db migration 

# try:
#     db.session.add(resource)
#     return db.session.commit()
# except exc.IntegrityError:
#     db.session.rollback()



with app.app_context():
    from models import User
    db.create_all()

from app import routes  # NOQA


