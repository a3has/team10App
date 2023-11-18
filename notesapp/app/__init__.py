from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'password',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# try:
#     db.session.add(resource)
#     return db.session.commit()
# except exc.IntegrityError:
#     db.session.rollback()

with app.app_context():
    from models import User
    db.create_all()

from app import routes  # NOQA
