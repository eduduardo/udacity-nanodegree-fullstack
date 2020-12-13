from os import environ
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from config import setup_db
from models import Actor, Movie


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_host = environ.get('DATABASE_HOST', "localhost:5432")
        self.database_name = "casting_agency"
        self.database_user = environ.get('DATABASE_USER', "app_user")
        self.database_path = "postgresql://{}@{}/{}".format(
            self.database_user, self.database_host, self.database_name)

        setup_db(self.app)

        self.new_actor = {
            "name": "Elijah Wood",
            "gender": "male"
        }

        self.new_movie = {
            "title": "Lord of the Rings",
            "release_date": "2001-12-13",
            "actors": [1]
        }

        self.token_assistant = environ.get('ASSISTANT_TOKEN', '')
        self.token_director = environ.get('DIRECTOR_TOKEN', '')
        self.token_producer = environ.get('PRODUCER_TOKEN', '')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    #--------------------------------------------------------------------------#
    # Actors
    #--------------------------------------------------------------------------#
    def test_400_if_authorized_and_create_actor_invalid(self):
        res = self.client().post('/actors', json={},
                                 headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad request")

    def test_401_if_unauthorized_and_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], "User has no create:actors on this resource")

    def test_200_if_authorized_and_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.name == self.new_actor['name']).order_by(
            Actor.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['actor'], actor.id)

    def test_400_if_authorized_and_update_actor(self):
        actor = Actor.query.order_by(Actor.id.desc()).first()

        res = self.client().patch('/actors/{}'.format(actor.id), json={},
                                  headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad request")

    def test_404_if_authorized_and_update_non_existing_actor(self):
        res = self.client().patch('/actors/999999999', json={},
                                  headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource could not be found")

    def test_401_if_unauthorized_and_update_actor(self):
        res = self.client().patch('/actors/999999999', json={},
                                  headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], "User has no update:actors on this resource")

    def test_200_if_authorized_and_update_actor(self):
        actor = Actor.query.order_by(Actor.id.desc()).first()

        new_name = 'Morgan Freeman'

        res = self.client().patch('/actors/{}'.format(actor.id), json={"name": new_name},
                                  headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['id'], actor.id)
        self.assertEqual(data['actor']['name'], new_name)

    def test_401_if_unauthorized_and_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['message'], 'Authorization is missing')

    def test_404_if_authorized_and_actors_invalid_pagitation(self):
        res = self.client().get('/actors?page=44444',
                                headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_200_if_authorized_and_get_all_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertGreater(len(data['actors']), 0)
        self.assertGreater(data['total'], 0)

    #--------------------------------------------------------------------------#
    # Movies
    #--------------------------------------------------------------------------#
    def test_200_if_authorized_and_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.title == self.new_movie['title']).order_by(
            Movie.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['movie'], movie.id)

    def test_400_if_authorized_and_create_invalid_movie(self):
        res = self.client().post('/movies', json={},
                                 headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad request")

    def test_401_if_unauthorized_and_create_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], "User has no create:movies on this resource")

    def test_200_if_authorized_and_update_movie(self):

        new_title = "Lord of The Rings: The Return of the King"

        movie = Movie.query.order_by(Movie.id.desc()).first()

        res = self.client().patch('/movies/{}'.format(movie.id),
                                  json={"title": new_title},
                                  headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], new_title)

    def test_400_if_authorized_and_update_invalid_movie(self):
        movie = Movie.query.order_by(Movie.id.desc()).first()

        res = self.client().patch('/movies/{}'.format(movie.id), json={},
                                  headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['message'], "Bad request")

    def test_404_if_authorized_and_update_non_existing_movie(self):
        res = self.client().patch('/movies/99999999999', json={},
                                  headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['message'], "Resource could not be found")

    def test_401_if_uauthorized_and_update_movie(self):
        res = self.client().patch('/movies/1', json={},
                                  headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(
            data['message'], "User has no update:movies on this resource")

    def test_404_if_movie_invalid_pagitation(self):
        res = self.client().get('/movies?page=44444',
                                headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_401_if_unauthorized_and_get_all_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['message'], 'Authorization is missing')

    def test_200_if_authorized_and_get_all_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertGreater(len(data['movies']), 0)
        self.assertGreater(data['total'], 0)

    #--------------------------------------------------------------------------#
    # Deletes test data at the end
    #--------------------------------------------------------------------------#
    # actor
    def test_404_if_authorized_and_delete_non_existing_actor(self):
        res = self.client().delete('/actors/999999999',
                                   headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource could not be found")

    def test_401_if_unauthorized_and_delete_actor(self):
        res = self.client().delete(
            '/actors/1', headers={"Authorization": 'Bearer ' + self.token_assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], "User has no delete:actors on this resource")

    def test_200_if_authorized_and_delete_actor(self):
        actor = Actor.query.order_by(Actor.id.desc()).first()

        res = self.client().delete('/actors/{}'.format(actor.id),
                                   headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor.id)

    # movies
    def test_404_if_authorized_and_delete_non_existing_movie(self):
        res = self.client().delete('/movies/999999',
                                   headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Resource could not be found")

    def test_401_if_unauthorized_and_delete_movie(self):
        res = self.client().delete(
            '/movies/1', headers={"Authorization": 'Bearer ' + self.token_director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.content_type, 'application/json')
        self.assertFalse(data['success'])
        self.assertEqual(
            data['message'], "User has no delete:movies on this resource")

    def test_200_if_authorized_and_delete_movie(self):
        movie = Movie.query.order_by(Movie.id.desc()).first()

        res = self.client().delete('/movies/{}'.format(movie.id),
                                   headers={"Authorization": 'Bearer ' + self.token_producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], movie.id)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
