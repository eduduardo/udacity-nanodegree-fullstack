#----------------------------------------------------------------------------#
# Models
#
# Obs: After several attempts to make the relationships right, I ended using the
# Association Object, which consists of 3 tables, in this case, "shows" links
# the artists and venues.
#
# source: https://stackoverflow.com/questions/38654624/flask-sqlalchemy-many-to-many-relationship-new-attribute
# SQLAlchemy docs about Association Object: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object
#----------------------------------------------------------------------------#
from config import *

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete="cascade"))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id', ondelete="cascade"))
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship("Venue", back_populates="artists")
    artist = db.relationship("Artist", back_populates="venues")

    def __repr__(self):
        return f'<Show {self.id} | {self.venue_id} | {self.artist_id} | {self.start_time}>'

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)

    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    artists = db.relationship("Show", back_populates="venue", lazy="dynamic")

    def __repr__(self):
        return f'<Venue {self.id} | {self.city} | {self.state} | {self.name} | {self.genres} | {self.seeking_talent}>'

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)

    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)

    venues = db.relationship("Show", back_populates="artist", lazy="dynamic")

    def __repr__(self):
        return f'<Artist {self.id} | {self.name}>'
