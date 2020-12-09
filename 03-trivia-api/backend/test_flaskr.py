from os import environ
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_host = environ.get('DATABASE_HOST', "localhost:5432")
        self.database_name = "trivia_test"
        self.database_user = environ.get('DATABASE_USER', "app_user")
        self.database_path = "postgres://{}@{}/{}".format(self.database_user, self.database_host, self.database_name)

        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the answer for the universe and everything else?',
            'answer': '42',
            'difficulty': 5,
            'category': 1 # Science
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'], True)
        self.assertTrue(data['total_categories'], True)
        self.assertEqual(len(data['categories']), data['total_categories'])

    def test_404_get_resource_not_found(self):
        res = self.client().get('/categoriesssssss')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_404_invalid_category(self):
        res = self.client().get('/categories/31231231203')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_first_page_questions_pagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)

        self.assertGreaterEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'], True)
        self.assertTrue(data['categories'], True)

    def test_more_pages_questions_pagination(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)

        self.assertTrue(data['questions'], True)
        self.assertTrue(data['total_questions'], True)
        self.assertTrue(data['categories'], True)

    def test_all_questions_beyond_pagination(self):
        res = self.client().get('/questions?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_delete_valid_question(self):
        random_question_to_delete = Question.query.limit(1).first()
        question_id = random_question_to_delete.id

        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_422_if_delete_invalid_question(self):
        res = self.client().delete('/questions/44141')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request could not be processable')

    def test_questions_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'Africa'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    def test_questions_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'Africdasdasa'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)

        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_400_questions_search_without_search_term(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_get_valid_pagination(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)

        self.assertTrue(data['questions'], True)
        self.assertTrue(data['current_category'], True)
        self.assertTrue(data['total_questions'], True)

        self.assertEqual(data['current_category'], 'Science')

    def test_invalid_pagitation(self):
        res = self.client().get('/categories/1/questions?page=44444')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # check if the question was inserted on the database
        question = Question.query.filter(Question.question == self.new_question['question']).order_by(Question.id.desc()).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], question.id)

    def test_400_if_question_creation_fails(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_get_first_random_quizz_question(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_random_quizz_category(self):
        res = self.client().post('/quizzes', json={"quiz_category": {"id": 1, "type": "Science"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 1)

    def test_get_random_quizz_without_previous(self):
        questions_ids = [x for x in range(1,10)]
        res = self.client().post('/quizzes', json={"previous_questions": questions_ids})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertNotIn(data['question']['id'], questions_ids)

    def test_get_random_quizz_ended(self):
        questions_ids = [x for x in range(1,1000)] # passing a lot of IDs, this will dry out every possibility of questions

        res = self.client().post('/quizzes', json={"previous_questions": questions_ids})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], True)
        self.assertIsNone(data['question'])

    def test_405_method_not_allowed(self):
        res = self.client().patch('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
