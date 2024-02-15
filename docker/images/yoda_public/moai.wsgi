import configparser
import os
import sys 

activate_this = '/var/www/moai/yoda-moai/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from paste.deploy import loadapp
from logging.config import fileConfig

config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'settings.ini')

try:
    fileConfig(config_file)
except (configparser.NoSectionError,KeyError):
    # no logging configured
    pass

application = loadapp('config:%s' % config_file)
