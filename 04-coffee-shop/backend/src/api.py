import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()
    if body is None:
        abort(400)

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if title is None or recipe is None:
        abort(400)

    # convert to string to properly store if the recipe is an array
    if type(recipe) is dict:
        recipe = [recipe]

    if recipe is not None:
        recipe = json.dumps(recipe)

    drink = Drink(title=title, recipe=recipe)

    drink.insert()

    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    body = request.get_json()

    if body is None:
        abort(400)

    try:
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        if title is not None:
            drink.title = title

        if recipe is not None:
            recipe = json.dumps(recipe)
            drink.recipe = recipe

        drink.update()

    except:
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    })


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except:
        abort(422)

    return jsonify({
        "success": True,
        "delete": drink_id
    })

# Error Handling


@app.errorhandler(401)
def bad_request(error):
    return jsonify({
        "error": 401,
        "message": "Unauthorized",
        "success": False
    }), 401


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
