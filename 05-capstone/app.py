# --------------------------------------------------------------------------- #
# Controllers
# --------------------------------------------------------------------------- #
from config import setup_db, db
from models import Actor, Movie, Cast
from flask_cors import CORS
from flask import Flask, request, abort, jsonify
from auth import requires_auth, AuthError

ACTORS_PER_PAGE = 5
MOVIES_PER_PAGE = 5


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,DELETE,OPTIONS')
        return response

    # index for check health
    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": 'healthy'
        })

    # ----------------------------------------------------------------------- #
    # Actors
    # ----------------------------------------------------------------------- #
    '''
  Endpoint to handle GET requests for actors, including pagination (every 5)
  This endpoint return a list of actors, their names, and movies participating
  '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        page = request.args.get('page', 1, type=int)
        actors = Actor.query.order_by(Actor.id)

        actors = actors.paginate(page=page, per_page=ACTORS_PER_PAGE)
        if actors is None:
            abort(404)

        return jsonify({
            "success": True,
            "actors": [actor.long() for actor in actors.items],
            "total": actors.total,
        })

    '''
  Endpoint to handle create an actor
  This endpoint return if success the actor ID, otherwise 400 or 422 errors
  '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        gender = body.get('gender', None)

        if name is None or gender is None:
            abort(400)

        actor = Actor(name=name, gender=gender)
        try:
            actor.insert()
        except:
            db.session.rollback()
            abort(422)

        return jsonify({
            "success": True,
            "actor": actor.id
        })
    '''
  Endpoint to handle update an actor
  This endpoint return if success the actor name and gender,
  otherwise 400 or 422 errors
  '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()

        if body is None:
            abort(400)

        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        name = body.get('name', None)
        gender = body.get('gender', None)

        if name is None and gender is None:
            abort(400)

        if name is not None:
            actor.name = name

        if gender is not None:
            actor.gender = gender

        try:
            actor.update()
        except:
            db.session.rollback()
            abort(422)

        return jsonify({
            "success": True,
            "actor": actor.short()
        })

    '''
  Endpoint to DELETE actor using a actor ID
  '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            actor.delete()
        except:
            db.session.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'deleted': actor_id
        })
    # ----------------------------------------------------------------------- #
    # Movies
    # ----------------------------------------------------------------------- #
    '''
  Endpoint to handle GET requests for movies, including pagination (every 5)
  This endpoint return a list of movies, their title, release_date
  and actors cast
  '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        page = request.args.get('page', 1, type=int)
        movies = Movie.query.order_by(Movie.id)

        movies = movies.paginate(page=page, per_page=MOVIES_PER_PAGE)
        if movies is None:
            abort(404)

        return jsonify({
            "success": True,
            "total": movies.total,
            "movies": [movie.long() for movie in movies.items],
        })
    '''
  Endpoint to handle create a new movie
  This endpoint return if success the movie ID, otherwise 400 or 422 errors
  '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)

        if title is None or release_date is None or actors is None:
            abort(400)

        movie = Movie(title=title, release_date=release_date)
        try:
            movie.insert()
        except:
            db.session.rollback()
            abort(422)

        for actor in actors:
            cast = Cast(movie_id=movie.id, actor_id=actor)
            cast.insert()

        return jsonify({
            "success": True,
            "movie": movie.id
        })
    '''
  Endpoint to handle update a movie
  This endpoint return if success the movie title, release_date and cast,
  otherwise 400 or 422 errors
  '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()

        if body is None:
            abort(400)

        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)

        if title is None and release_date is None and actors is None:
            abort(400)

        if title is not None:
            movie.title = title

        if release_date is not None:
            movie.release_date = release_date

        if actors is not None:
            movie.actors = actors

        try:
            movie.update()
        except:
            db.session.rollback()
            abort(422)

        return jsonify({
            "success": True,
            "movie": movie.long()
        })

    '''
  Endpoint to DELETE movie using a movie ID
  '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()
        except:
            db.session.rollback()
            abort(422)

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    # ----------------------------------------------------------------------- #
    # Error handlers for expected errors
    # imported from previous udacity projects
    # ----------------------------------------------------------------------- #

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": 400,
            "message": "Bad request",
            "success": False
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": 404,
            "message": "Resource could not be found",
            "success": False
        }), 404

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "error": 405,
            "message": "Method not allowed",
            "success": False
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "error": 422,
            "message": "Request could not be processable",
            "success": False
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "error": 500,
            "message": "Internal server error",
            "success": False
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
