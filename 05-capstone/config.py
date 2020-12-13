#----------------------------------------------------------------------------#
# App Configs
#----------------------------------------------------------------------------#
from os import environ
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Binds a Flask application with the SQLAlchemy service

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
