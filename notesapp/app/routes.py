from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from forms import *
from flask_login import current_user, login_user, logout_user, login_required
from models import *
from werkzeug.urls import url_parse
from forms import RegistrationForm, AdvancedSearchForm, NoteForm, RegexSearchForm
import google.auth
from googleapiclient.discovery import build
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
import re
import google.oauth2.credentials
import google_auth_oauthlib.flow
from models import Note, Tag, note_tags
import pandas as pd
import plotly.express as px
from sqlalchemy import func


with app.app_context():

    # secret file needed for api access. pls dont leak
    CLIENT_SECRETS_FILE = "app/client_secret.json"
    # calendar will only read non sensitive info
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def credentials_to_dict(credentials):  # each user is listed into a dict
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}


# test login to see if its working, prints test table given by google documentation
@app.route('/testlogin')
def index():
    return print_index_table()


# sends you to the google authorization login screen
@app.route('/Googlelogin')
def Googlelogin():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)


# after authentication from google flow, this sends you back the credidentials to /calendar
@app.route('/oauth2callback')
def oauth2callback():

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect('/calendar')
    # return redirect(url_for('Googlelogin'))
    # return redirect(url_for('calendarBasic'))
    # return redirect('/calendarBasic')
    # return redirect(url_for('testlogin'))
    # return redirect('/testlogin')


@app.route('/revoke')  # logs your google account out after leaving pages
def revoke():
    if 'credentials' not in session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    revoke = request.post('https://oauth2.googleapis.com/revoke',
                          params={'token': credentials.token},
                          headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return ('Credentials successfully revoked.' + print_index_table())
    else:
        return ('An error occurred.' + print_index_table())


def print_index_table():  # the index table used for testing
    return ('<table>' +
            '<tr><td><a href="/test">Test an API request</a></td>' +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr></table>')


@app.route('/clear')  # deletes all google creds on demand
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())


# imports your events from your personal google calendar.
@app.route('/calendar')
def calendar():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next events. all info printed is not sensitive.
        formatted_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            formatted_events.append((start, event["summary"]))

    except HttpError as error:
        print(f"An error occurred: {error}")

    # returns the display function
    return render_template('calendar.html', results=formatted_events)


# simple calendar embed without needing to login.
@app.route('/calendarBasic', methods=['GET', 'POST'])
def Gcal():
    return render_template('calendarBasic.html')


# send to login screen with all login features.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# also sends you to home if logged in.
@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
@login_required
def home():
    return render_template('home.html') # redirect to home page 

# route for viewing notes. Crud operations accessible from here
@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NoteForm()
    all_tags=Tag.query.order_by(Tag.name).all()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            body=form.note.data,
            color=form.color.data,
            author=current_user)
        for tag_name in form.tags.data.split(','):
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.session.add(tag)
            note.tags.append(tag)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes'))
    else:
        selected_tag = request.args.get('tag')
        if selected_tag:
            posts = Note.query.join(Note.tags).filter(Tag.name == selected_tag, Note.user_id == current_user.id).all()
        else:
            posts = current_user.get_notes()
    return render_template('notes.html', title='Home Page', form=form, posts=posts, tags=all_tags)


@app.route('/register', methods=['GET', 'POST'])  # registers new user.
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user', methods=['GET', 'POST']) # handle get and post request 
def profile(): # profile page 
    form = EditProfileForm() # created form using edit profile form  
    user = User.query.get_or_404(current_user.id) # get user from data base 

    if form.validate_on_submit(): # if validated update user information 
        user.username = form.username.data
        user.email = form.email.data
        user.biography = form.biography.data
        db.session.commit() # save changes 
        # Redirect to avoid post/redirect/get pattern
        return redirect(url_for('profile'))

    elif request.method == 'GET': # if request is to get then udpdate information 
        form.username.data = user.username
        form.email.data = user.email
        form.biography.data = user.biography

    note_count = user.notes.count() # count the number of notes for the user 
    return render_template('user.html', title='User Profile', form=form, user=user, note_count=note_count)


@app.route('/todo')
def todo():
    todo_list = Todo.query.filter_by(user_id=current_user.id).all() # create todo for unique users 
    # todo_list = current_user.Todo.all()
    # todo_list=Todo.query.all()
    return render_template('todo.html', todo_list=todo_list) # user redered hmtl template 


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name") # gt name from form
    new_task = Todo(name=name, done=False, user_id=current_user.id) # new task for unique users 
    db.session.add(new_task) # add task to db 
    db.session.commit() # commmit to db 
    return redirect(url_for("todo")) # rediect 


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id) # get todo id from data base 
    todo.done = not todo.done # toggle wheter task is done or not 
    db.session.commit() # commit to db 
    return redirect(url_for("todo"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id) # get todo id from data base 
    db.session.delete(todo) # delete the task from db 
    db.session.commit() # commit 
    return redirect(url_for("todo")) #redirect 

@app.route('/advanced_searching', methods=['GET', 'POST'])
def advanced_search():
    form_todo = AdvancedSearchForm()  # AdvancedSearchForm for Todo
    form_note = AdvancedSearchNoteForm()  # AdvancedSearchNoteForm for Note

    results_todo, results_note = [], []

    if form_todo.validate_on_submit() or form_note.validate_on_submit():

        # Clear the existing search results before performing a new search
        results_todo, results_note = [], []

        if form_todo.task_name.data:
            query_todo = Todo.query.filter_by(user_id=current_user.id)

            query_todo = query_todo.filter(Todo.name.ilike(f'%{form_todo.task_name.data}%'))

            # Filter based on completion status
            query_todo = query_todo.filter(Todo.done == form_todo.is_complete.data)

            results_todo = query_todo.all()

        if form_note.title.data or form_note.body.data or form_note.tag.data:
            query_note = Note.query.filter_by(user_id=current_user.id)

    

            if form_note.body.data:
                query_note = query_note.filter(Note.body.ilike(f'%{form_note.body.data}%'))

            if form_note.tag.data:
                query_note = query_note.filter(Note.tags.any(Tag.name.ilike(f'%{form_note.tag.data}%')))

            results_note = query_note.all()

        # Render the search results page if there are results in either todo list or note search
        if results_todo or results_note:
            return render_template('search_results.html', form_todo=form_todo, form_note=form_note, results_todo=results_todo, results_note=results_note)

    # Render the search page with the form and no results initially
    return render_template('adv_search.html', form_todo=form_todo, form_note=form_note, results_todo=None, results_note=None)

@app.route('/regex_search', methods=['GET', 'POST'])
def regex_search():
    form = RegexSearchForm()  #RegexSearchForm

    results_todo, results_note = [], []

    if form.validate_on_submit():
        # Clear the existing search results before performing a new search
        results_todo, results_note = [], []

        search_query = form.regex_query.data

        if search_query:
            # Perform regex search for todos
            query_todo = Todo.query.filter_by(user_id=current_user.id)
            query_todo = query_todo.filter(Todo.name.op('REGEXP')(search_query))
            results_todo = query_todo.all()

            # Perform regex search for notes
            query_note = Note.query.filter_by(user_id=current_user.id)
            query_note = query_note.filter(
                (Note.title.op('REGEXP')(search_query)) | (Note.body.op('REGEXP')(search_query))
            )
            results_note = query_note.all()

        # Render the search results page if there are results in either todo list or note search
        if results_todo or results_note:
            return render_template('regex_search_results.html', form=form, results_todo=results_todo, results_note=results_note)

    # Render the regex search page with the form and no results initially
    return render_template('regex_search.html', form=form, results_todo=None, results_note=None)


@app.route('/logout')  # logs out the user.
def logout():
    logout_user()
    return redirect(url_for('login'))

# route for editing existing notes on the /notes route
@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.note.data
        note.color = form.color.data
        note.tags = []
        for tag_name in form.tags.data.split(','):  # Assuming tags are comma-separated
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.session.add(tag)
            note.tags.append(tag)
        db.session.commit()
        return redirect(url_for('notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.note.data = note.body
        form.color.data = note.color
        form.tags.data = ', '.join([tag.name for tag in note.tags])  # Convert tags to a comma-separated string
    return render_template('edit_note.html', title='Edit Note', form=form, note_id=note.id)

# route for deleting existing notes on the /notes route
@app.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/note_visualization')
def note_visualization():
    # Extract date information from notes
    date_counts = db.session.query(func.date(Note.timestamp).label('date'), func.count().label('note_count')).group_by('date').all()

    # Extract tag information from notes
    tag_counts = db.session.query(Tag.name.label('tag_name'), func.count().label('note_count')).join(note_tags).group_by(Tag.name).all()

    # Convert Row objects to dictionaries for easy serialization
    date_counts = [{'date': entry.date, 'note_count': entry.note_count} for entry in date_counts]
    tag_counts = [{'tag_name': entry.tag_name, 'note_count': entry.note_count} for entry in tag_counts]

    return render_template('note_visualization.html', title='Note Visualizations', date_counts=date_counts, tag_counts=tag_counts)