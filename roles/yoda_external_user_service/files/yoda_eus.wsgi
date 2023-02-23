#!/usr/bin/env python3

import os
import sys

activate_this = '/var/www/extuser/yoda-external-user-service/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from yoda_eus import app

application = app.create_app(config_filename="/var/www/extuser/flask.cfg")
