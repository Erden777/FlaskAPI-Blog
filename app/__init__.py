import os
import logging
from os.path import join, dirname, abspath, exists
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from .db import db_init
from app.log import setup_logger
from flask_bcrypt import Bcrypt
    
base_dir = dirname(dirname(abspath(__file__)))
config_file = join(base_dir, 'config.py')
env_file = join(base_dir, '.env')

app = Flask(
    __name__,
    instance_relative_config=False,
    root_path=base_dir,
)


bcrypt = Bcrypt(app)
from app.marshmellow import init_ma
init_ma(app)

from app.routes import auth_blueprint
app.register_blueprint(auth_blueprint)

if exists(env_file):
    app.config.from_pyfile(config_file)
    load_dotenv(dotenv_path=env_file)


if app.config['DEBUG']:

    print(' * working logger')
    fh = setup_logger('app', 'app/logs/error.log', logging.ERROR)
    
CORS(app, supports_credentials=True)
db_init(app, create=True)


