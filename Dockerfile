# syntax=docker/dockerfile:1
# pull the official base image, [tagname]:[version]: (python:3.8 is the defacto image. If you are unsure about what your needs are, you probably want to use this one. )
FROM python:3.8
# python:<version>-slim ==> This image does not contain the common packages contained in the default tag and only contains the minimal packages needed to run python. 
# python:<version>-alpine ==> This image is based on the popular Alpine Linux project, available in the alpine official image. Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general.

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG=0

# install dependencies
WORKDIR /app

# Install Customized system dependencies
# install psycopg2 dependencies
# RUN apk update
# RUN apk add postgresql-dev musl-dev 
# RUN apt-get install -qy python3-dev postgresql-dev build-essential
# RUN pip install pyzmq
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# copy requirements.txt to /app/requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip 
# Install project dependencies to entire system with pipenv
# RUN pip3 install pipenv
# RUN pipenv install -r requirements.txt
# RUN pipenv shell
# RUN pipenv install django==3.1.1 gunicorn --python 3.8
# RUN pipenv install --skip-lock --system --dev
RUN pip3 install -r requirements.txt
# python -m venv venv
# echo venv/ >> .gitignore
# source venv/bin/activate
# RUN pip3 freeze

# copies all the project source code to the working directory in the container.
COPY . .

# 8000 is default for Django to be exposed(so we can access the container from localhost, or even anywhere at internet)
EXPOSE 8000
ENV PORT 8000


# FOR Node.js use
# 3000 is default for Node.js
# ENV PORT 3000
# EXPOSE 3000
# COPY package.json /code/package.json
# RUN npm install


# For Flask
# ENV FLASK_DEBUG 0
# 5000 is default for Flask
# ENV PORT 5000
# EXPOSE 5000


# sets the executable commands in the container.
# RUN python chatbot/manage.py migrate
CMD ./launch.sh
# CMD ["python3", "chatbot/manage.py", "runserver", "0.0.0.0"]
# CMD gunicorn app_name.wsgi:application --bind 0.0.0.0:$PORT
# EXPOSE 3000
# CMD ["npm", "start"]
# EXPOSE 5000
# CMD ["flask", "run", "--host=0.0.0.0", "-p", "5001"]
# 8888 is default for Jupyter Notebook


# Build a image and Run a container
# docker build -t hello_world_app .
# docker run -it -p 5000:5000 hello_world_app 


## Extra command
# lsb_release -a
# wsl -l -v

# Publishing the Docker image to Docker Hub
# docker login
# docker tag django_todo:latest <Docker Hub username>/django_todo:latest
# docker push <Docker Hub username>/django_todo:latest

# Deploy to Heroku
# heroku login
# heroku container:login
# heroku container:push web
# heroku container:release web
# heroku open
# curl http://cse5914-2020fall.herokuapp.com/api/get_latest_movie/

# Reference:
# Section: https://www.section.io/engineering-education/django-docker/
# Semaphore Dockerizing a Python Django Web Application: https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application
# Basic Usage of Pipenv: https://pipenv-fork.readthedocs.io/en/latest/basics.html
# Django on Docker Tutorial - A Simple Introduction, https://www.youtube.com/watch?v=KaSJMDo-aPs
# Flask on Docker Example, https://docs.docker.com/language/python/build-images/
# 