from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from forms import *
from flask_login import current_user, login_user, logout_user, login_required
from models import *
from werkzeug.urls import url_parse
from forms import RegistrationForm, AdvancedSearchForm, NoteForm
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

import google.oauth2.credentials
import google_auth_oauthlib.flow

with app.app_context():

    CLIENT_SECRETS_FILE = "app/client_secret.json"
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def credentials_to_dict(credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}


@app.route('/testlogin')
def index():
    return print_index_table()


@app.route('/Googlelogin')
def Googlelogin():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)


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


@app.route('/revoke')
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


def print_index_table():
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


@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())


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

        # Prints the start and name of the next 10 events
        formatted_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            formatted_events.append((start, event["summary"]))

    except HttpError as error:
        print(f"An error occurred: {error}")

    return render_template('calendar.html', results=formatted_events)


@app.route('/calendarBasic', methods=['GET', 'POST'])
def Gcal():
    return render_template('calendarBasic.html')


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


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# route for viewing notes. Crud operations accessible from here
@app.route('/notes', methods=['GET', 'POST'])
def notes():
    form = NoteForm()
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
        print(form.errors)
    posts = current_user.get_notes()
    return render_template('notes.html', title='Home Page', form=form, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/user', methods=['GET', 'POST'])
def profile():
    form = EditProfileForm()
    user = User.query.get_or_404(current_user.id)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.biography = form.biography.data
        db.session.commit()
        # Redirect to avoid post/redirect/get pattern
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.biography.data = user.biography

    note_count = user.notes.count()
    return render_template('user.html', title='User Profile', form=form, user=user, note_count=note_count)

@app.route('/todo')
def todo():
    todo_list = Todo.query.filter_by(user_id=current_user.id).all()
    # todo_list = current_user.Todo.all()
    # todo_list=Todo.query.all()
    return render_template('todo.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    new_task = Todo(name=name, done=False, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/advanced_searching', methods=['GET', 'POST'])
def advanced_search():
    form = AdvancedSearchForm()

    if form.validate_on_submit():
        # Build the query based on form input
        query = Todo.query.filter_by(user_id=current_user.id)
        # query = Todo.query

        if form.task_name.data:
            query = query.filter(Todo.name.ilike(f'%{form.task_name.data}%'))

        if form.is_complete.data is not None:
            query = query.filter(Todo.done == form.is_complete.data)

        # Execute the query for all
        results = query.all()

        return render_template('search_results.html', results=results)

    return render_template('adv_search.html', form=form)


@app.route('/logout')
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
