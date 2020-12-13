# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
from config import db

'''
Extend the base Model class to add common methods
'''
class BaseModel(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# cast is the many-to-many relationship of actors and movies


class Cast(BaseModel):
    __tablename__ = 'cast'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete="cascade"))
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'actors.id', ondelete="cascade"))

    movie = db.relationship("Movie", back_populates="actors")
    actor = db.relationship("Actor", back_populates="movies")

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def __repr__(self):
        return f'<Cast {self.movie_id} | {self.actor_id}>'


class Movie(BaseModel):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    actors = db.relationship("Cast", back_populates="movie", lazy="dynamic")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def long(self):
        actors = []
        for cast in self.actors.all():
            actors.append(cast.actor.short())

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d"),
            'actors': actors
        }

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d"),
        }

    def __repr__(self):
        return f'''<Movie {self.id} | {self.title} |
                {self.release_date.strftime("%Y-%m-%d")}>'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, default='male')

    movies = db.relationship("Cast", back_populates="actor", lazy="dynamic")

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        movies = []
        for movie in self.movies.all():
            if movie.movie is not None:  # an actor maybe in no movie yet!
                movies.append(movie.movie.short())

        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'movies': movies
        }

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
        }

    def __repr__(self):
        return f'<Actor {self.id} | {self.name} | {self.gender}>'
