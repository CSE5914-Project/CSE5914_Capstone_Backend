#!/bin/bash
# PORT=8000
python3 chatbot/manage.py runserver 0.0.0.0:$PORT
# export FLASK_APP=project.server
# export APP_SETTINGS="project.server.config.DevelopmentConfig"
# flask db init
# python chatbot/manage.py migrate
# flask db upgrade
#flask run --host=0.0.0.0 --port=5000
# flask run