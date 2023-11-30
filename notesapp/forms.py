from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from models import User
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    note = CKEditorField('Content', validators=[DataRequired()])
    color = SelectField(
        'Background Color',
        choices=[
            ('#e7e7e7', 'Default'),      # Pastel gray
            ('#daf0f7', 'Blue'),      # Pastel blue
            ('#77dd77', 'Green'),     # Pastel green
            ('#fdfd96', 'Yellow'),    # Pastel yellow
            ('#ff6961', 'Red'),       # Pastel red
            ('#b19cd9', 'Purple'),    # Pastel purple
            ('#ffb347', 'Orange'),    # Pastel orange
            ('#ffbfd3', 'Pink'),      # Pastel pink
            ('#cfcfc4', 'Brown'),     # Pastel brown
            ('#aec6cf', 'Cyan')       # Pastel cyan
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
    
class AdvancedSearchForm(FlaskForm): # set varibles like task name sumb and compelted 
    task_name = StringField('Task Name') 
    is_complete = BooleanField('Completed')
    submit = SubmitField('Search')

class EditProfileForm(FlaskForm): # set user name email and bio 
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    biography = TextAreaField('Biography', validators=[Length(max=500)])
    submit = SubmitField('Save Changes')