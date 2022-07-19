# django_backend


## Overview

API
+ GetMovie
+ GetQuestion
+ PostAnswer


### TODO

#### ckpt 1
+ [x] Basic API
+ [ ] Movie Model
+ [ ] User Model
+ [ ] Implement Session


## App deployment:

- Reference:
  - https://docs.google.com/document/d/1W57Pf48E5z1Zg8dsoWrZd1FxkHIqCSrgStXAvqLGQYQ/edit#heading=h.jwaty07wsref
```bash
#You need a Procfile to work with heroku, read more here https://devcenter.heroku.com/articles/procfile
# <process type>: <command>
web: gunicorn app:app	
# 'web' is tye process type
# 'gunicorn app:app' is the command, with format $ gunicorn [OPTIONS] [WSGI_APP] --> It say we will look for a python file, app.py, and run a variable called app

# Make a clean commit
git add .
git commit -m "commit"

# Push to remote endpoint at heroku, with branch main
heroku login 
# If it's first time:
# heroku apps:create students-flask 	
git push heroku main

# Check any error
heroku logs --tail
```

## How to run
```bash
set FLASK_APP=back_end.py
flask run
```

## Create virtual env
```bash
# Install virtual env
python3 -m pip install --user virtualenv

#Linux/Mac
python3 -m venv venv  
source venv/bin/activate
#Windows
py -m venv venv  
# env\Scripts\activate.bat	
.\venv\Scripts\activate

# Intall required packages using:
pip install -r requirements.txt
```
