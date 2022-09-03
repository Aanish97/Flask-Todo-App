import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import APP_CONFIG

# initializing app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = APP_CONFIG.get('development').SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = APP_CONFIG.get('development').SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = APP_CONFIG.get('development').SECRET_KEY
app.config['DEBUG'] = os.getenv('DEBUG')
app.config.from_object(APP_CONFIG["development"])


# initializing database
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
