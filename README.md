# CMPE_131_StickyNotes_Web

### Table of Contents
- [Introduction](#introduction)
- [Collaborators](#collaborators)
- [Project Setup](#project-setup)
- [Packages](#packages)
- [Requirements](#requirements)
- [How To Use](#how-to-use)
- [Pull Request](#pullrequest)

## Introduction
For this project we are building a webpage that stores online notes. Our website called StickyNotes implements a basic structure of note taking, supporting featrues such as login, logout, password hashing, todo, searching, user profiles, and editing notes text.   

## Collaborators 
- Sammy Cuaderno (@Scuaderno1991)
- Abdulkader Hasbini (@a3has)
- Jonathan Nguyen (@jonathanguven) Team Lead
- Nikko Timbol (@franznikko)

## Project Setup
1. Clone this repository on your own local machine
```bash
# clone github project
git clone git@github.com:a3has/team10App.git

# navigate into project directory
cd team10App/notesapp
```
2. Create and activate a virtual environment in the `/notesapp` directory
```bash
# in the /team10App/notesapp directory
python3 -m venv venv
source venv/bin/activate
```
3. Install all necessary requirements 
```bash
# install from requirements.txt file
pip3 install -r requirements.txt
```
4. Downgrade Werkzeug to working version
```bash
pip3 install werkzeug==2.2.2
```
5. Start the flask application
```bash
flask run
```

## How To Use
### Login
1. You will initially be prompted to login. Click the link to create an account.
2. Create an account. You will then be successfully logged in and redirected to the project /home route.

### View Notes
1. From the /home route, click on the `Notes` button. This leads you to the /notes route
2. All of your created notes will be displayed on this page, along with a button to create a note and a button to go navigate back to the home page.

### Create Note
1. From the /home route, navigate to the /notes route usign the `Notes` button.
2. Click the green button labeled `Create Note`. This causes a form for note creation to show up. 
3. Fill in the `Title` field with the title of the note you are creating.
4. Fill in the `Content` field with the title of the note you are creating.
5. Optionally, select the background color of your note. 
6. Click the submit button upon filling out the title and content fields.
7. Your note is successfully created, and you will see it on the web page.

### Edit Note
1. From the /home route, navigate to the /notes route.
2. You must have at least 1 note created and viewable on the web page.
3. Click on the blue `edit` button on the top right of the note you want to edit.
4. A form will show up with editable title, content, and background color select fields, with their original contents already stored within the fields.
5. Edit the title, content, and color fields as needed.
6. Click the submit button to finalize the edits.
7. You will be redirected back to the notes web page, and you will see the edited note with the new content.

### Delete Note
1. From the /home route, navigate to the /notes route.
2. You must have at least 1 note created and present on the web page.
3. Click on the red `delete` button on the top right of the note you wish to delete.
4. You will be prompted to confirm you wish to delete the selected note. Click 'Ok'.
5. The note will be deleted, and you will no longer see it on the web page.

### Edit Profile
1. From the /home route, navigate to the /user directory using the `User Profile` button. 
2. Click the `edit` button underlined under the page header.
3. A form will show up allowing you to edit your username, email, and biography.
4. Edit which fields you wish to change, and click submit.
5. Your web page should now show the new profile changes that you set.

### Logout
1. From the /home route, click the `Logout` button. 
2. You will then be logged out, and redirected back to the /login route.

## Packages
Find a list of the packages we used for this application [here](https://github.com/a3has/team10App/blob/milestone2/notesapp/requirements.txt).

## Requirements 
    - To Do Checklist (Sammy)
    - Search (Sammy)
    - Homepage (Sammy)
    - Search (Sammy)

## PullRequest
- [SammyPull](https://github.com/a3has/team10App/commit/bb241d9ac4581173bcae478580cd8f3db60c4f9d)

- [SammyPull1](https://github.com/a3has/team10App/commit/3e74ca9e8ae35721fb2de6e0f6e532d04687d0c7)

- [SammyPull2](https://github.com/a3has/team10App/commit/6df975e8fcc909d60aea1e8e59f1ec4e3ace9069)

- [SammyPull3](https://github.com/a3has/team10App/commit/3e74ca9e8ae35721fb2de6e0f6e532d04687d0c7)
