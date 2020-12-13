#----------------------------------------------------------------------------#
# App Configs
#----------------------------------------------------------------------------#
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configs to connect to the database
database_host = environ.get('DATABASE_HOST', "localhost:5432")
database_name = environ.get('DATABASE_NAME', "casting_agency")
database_user = environ.get('DATABASE_USER', "app_user")
database_path = "postgresql://{}@{}/{}".format(database_user, database_host, database_name)

db = SQLAlchemy()

# Binds a Flask application with the SQLAlchemy service and Flask Migrate
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
