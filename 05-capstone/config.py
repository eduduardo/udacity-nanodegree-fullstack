#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

database_path = environ.get('DATABASE_URL', 'postgresql://app_user@localhost:5432/casting_agency')

# Binds a Flask application with the SQLAlchemy service and Flask Migrate
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
