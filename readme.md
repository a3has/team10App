# CMPE_131_StickyNotes_Web

### Table of Contents
- [Introduction](#Introduction)
- [Collaborators](#Collaborators)
- [Installation](#Installation)
- [Run](#Run)
- [Packages](#Packages)
- [Usage](#Usage)
- [Requirements](#Requirements)
- [HowToUseWebsite](HowToUseWebsite)
- [PullRequest](PullRequests)

## Introduction
    For this project we are building a webpage that stores online notes. Our website called StickyNotes implements a basic structure of note taking, supporting featrues such as login, logout, password hashing, todo, searching, user profiles, and editing notes text.   

## Collaborators 
    - Sammy Cuaderno (@Scuaderno1991)
    - Abdulkader Hasbini (@a3has)
    - Jonathan Nguyen (@jonathanguven) Team Lead
    - Nikko Timbol (@franznikko)

## Installations
    - Linux Distribution
    -Windows User 
        - Downlaod Ubuntu from Microsoft Store 
        - Enable Windows Subsystem for Linux (WSL) via Windows Features

    -Mac Users
        - Install Brew 
            /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        - brew install bash
        - check version 
            echo $BASH_VERSION
    - Python 3
        - sudo apt-get install python3 
        - sudo apt-get upgrade
        - python3 --version  

## Run
    To run our application you must first create a virtual environment. Create this virtual environment to encapsulate the whole program. After you create a virtual environment you must activate it. Once you are in the virtual environment, you must install the required packes from the requirements.txt file located in team10App/notesapp and then check to see if the packages were installed.

        - python3 -m venv PreferNameOfVirtualEnvironment
        - source PreferNameOfVirtualEnvironment/bin/activate
        - pip3 install -r team10App/notesapp/requirements.txt
        - pip3 freeze 
        - cd team10App/notesapp
        - flask run 
## Packages
    These packages are required for the functionalty of the programs to work. Without these packages, you will run into errors so install all of them. 
        alembic==1.12.1
        blinker==1.7.0
        click==8.1.7
        dnspython==2.4.2
        email-validator==2.1.0.post1
        Flask==3.0.0
        Flask-CKEditor==0.5.0
        Flask-Login==0.6.3
        Flask-Migrate==4.0.5
        Flask-SQLAlchemy==3.1.1
        Flask-WTF==1.2.1
        greenlet==3.0.1
        idna==3.4
        itsdangerous==2.1.2
        Jinja2==3.1.2
        Mako==1.3.0
        MarkupSafe==2.1.3
        python-dotenv==1.0.0
        SQLAlchemy==2.0.23
        typing_extensions==4.8.0
        Werkzeug==2.2.2
        WTForms==3.1.1

## Requirements 

    - To Do Checklist (Sammy)
    - Search (Sammy)
    - Homepage (Sammy)
    - Search (Sammy)

## HowToUseWeb
    To use our website you must first created an account using the signup button. Here it will ask you for a valid email, password, and username. After you have created an account you can log into the website with your credentials. You can edit profile and update your name and biography, create a todo list and mark it complete or not complete, create notes and saving them with a title and text, search todo checklist of items not completed, and logout of the website. You cna create as many accounts as long as the username and email isnt already being used.   

## PullRequest
- [SammyPull](https://github.com/a3has/team10App/commit/bb241d9ac4581173bcae478580cd8f3db60c4f9d)

- [SammyPull1](https://github.com/a3has/team10App/commit/3e74ca9e8ae35721fb2de6e0f6e532d04687d0c7)

- [SammyPull2](https://github.com/a3has/team10App/commit/6df975e8fcc909d60aea1e8e59f1ec4e3ace9069)

- [SammyPull3](https://github.com/a3has/team10App/commit/3e74ca9e8ae35721fb2de6e0f6e532d04687d0c7)




































