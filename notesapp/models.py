from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id): # laod users 
    return User.query.get(int(id))


class User(UserMixin, db.Model): # set fields for all users 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='author', lazy='dynamic')
    biography = db.Column(db.Text, nullable=True)
    def set_password(self, password): # generate a password hash 
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # check password hash 
        return check_password_hash(self.password_hash, password)

    def get_notes(self):
        return self.notes.order_by(Note.timestamp.desc()).all()

    def __repr__(self):
        return '<User {}>'.format(self.username)

# db model for individual notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    color = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}: {}>'.format(self.title, self.body)

class Todo(db.Model): # create colums for taskid, name and userid 
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    done=db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    notes = db.relationship('Note', secondary=note_tags, lazy='subquery',
                            backref=db.backref('tags', lazy='dynamic'))