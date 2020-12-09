import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# inspired by the udacity example


def format_output(selection):
    entities = [entity.format() for entity in selection]
    return entities


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

    '''
  Endpoint to get all available categories
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        categories_formated = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': categories_formated,
            'total_categories': len(categories)
        })

    '''
  Endpoint to handle GET requests for questions, including pagination (every 10 questions).
  This endpoint return a list of questions, number of total questions, current category, categories.
  '''
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        current_category = request.args.get('current_category', type=int)

        questions = Question.query.order_by(Question.id)

        if current_category is not None:
            questions = questions.filter_by(category=current_category)

        '''
      Using the SQLAlchemy pagination solution. It's not correct to use all(),
      bring all data from the database, and slice the array[start:end],
      doing this we are processing a large amount of data we download all data
      in the memory and most of it will be not sent to the client,
      this is the responsibility of the database
      '''
        questions = questions.paginate(page=page, per_page=QUESTIONS_PER_PAGE)
        if questions is None:
            abort(404)

        questions_formated = format_output(questions.items)

        categories = Category.query.order_by(Category.id).all()
        categories_formated = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': questions_formated,
            'total_questions': questions.total,
            'current_category': current_category,
            'categories': categories_formated
        })

    '''
  Endpoint to DELETE question using a question ID
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    '''
  Endpoint to create a new question, which requires the question and answer text, category, and difficulty score.
  Also is the endpoint to get questions based on a search term. It returns any questions for whom the search term is a substring of the question.
  '''
    @app.route('/questions', methods=['POST'])
    def add_or_search_questions():
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        search_term = body.get('searchTerm', None)

        if search_term:
            page = request.args.get('page', 1, type=int)
            questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')) \
                                      .order_by(Question.id) \
                                      .paginate(page=page, per_page=QUESTIONS_PER_PAGE)

            questions_formated = format_output(questions.items)

            return jsonify({
                'success': True,
                'questions': questions_formated,
                'total_questions': questions.total
            })

        else:
            if title is None or answer is None or difficulty is None or category is None:
                abort(400)

            try:
                question = Question(
                    question=title, answer=answer, difficulty=difficulty, category=category)
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id
                })
            except:
                abort(422)

    '''
  Endpoint to get questions based on category
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)

        current_category = Category.query.filter_by(
            id=category_id).one_or_none()
        if current_category is None:
            abort(404)

        questions = Question.query.filter_by(category=category_id) \
                                  .order_by(Question.id) \
                                  .paginate(page=page, per_page=QUESTIONS_PER_PAGE)
        if questions is None:
            abort(404)

        items = format_output(questions.items)

        return jsonify({
            'success': True,
            'questions': items,
            'current_category': current_category.type,
            'total_questions': questions.total
        })

    '''
  Endpoint to get questions to play the quiz. This endpoint take category and
  previous question parameters and return a random questions within the given category,
  if provided, and that is not one of the previous questions.
  '''
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        try:
            body = request.get_json()

            if body is not None:
                previous_questions = body.get('previous_questions', None)
                quiz_category = body.get('quiz_category', None)
            else:
                previous_questions = None
                quiz_category = None

            question = Question.query

            # Using https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_
            # this will not include all the IDs passed on the request args
            if previous_questions is not None:
                question = question.filter(
                    Question.id.notin_(previous_questions))

            if quiz_category is not None and quiz_category['id'] != 0:
                question = question.filter_by(category=quiz_category['id'])

            # Using build in random SQLAlchemy function
            # ref: https://stackoverflow.com/a/60815/6454864
            question = question.order_by(func.random()).limit(1).first()

            if question is not None:
                question = question.format()

            return jsonify({
                'success': True,
                'question': question
            })
        except:
            abort(422)

    '''
  Error handlers for expected errors
  '''
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

    return app
