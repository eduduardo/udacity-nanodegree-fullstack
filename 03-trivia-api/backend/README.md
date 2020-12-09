# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export DATABASE_HOST=localhost:5432
export DATABASE_NAME=trivia
export DATABASE_USER=app_user
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Documentation
### GET **`/categories`**
Endpoint to get all available categories, which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

### GET **`/questions`**
Endpoint to get all for questions, including pagination (every 10 questions).
- Request Arguments:
```
/questions?current_category=1 (optional) - ID correspondent to category, example: 1 - Science
/questions?page=1 (optional) - number of the correspondent page
```
- Returns: An object with the questions paginated and filtered if current_category is provided or return all questions
```
{
  "questions": [
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "success": true,
  "total_questions": 3
}
```

### DELETE **`/questions/<int:question_id>`**
Endpoint to DELETE question using a question ID
- Request Arguments:
```
question_id - question ID to remove
ex.: /questions/10
```
- Returns: An object with the `deleted` question ID if success, if not return 422 error.
```
{
  "deleted": 42,
  "success": true
}
```

### POST **`/questions`**
The endpoint to create a new question, which requires the question and answer text, category, and difficulty score. Also is the endpoint to get questions based on a search term. It returns any questions for whom the search term is a substring of the question.

- Request Arguments:
1. if searching use:
```
{
    "searchTerm": "American"
}
```
2. if creating a new question use:
```
{
    "question": "What is the answer for the universe and everything else?",
    "answer": "42",
    "difficulty": 5,
    "category": 1
}
```
- Returns:
1. if searching:
```
{
  "questions": [
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
2. if creating a new question use:
```
{
  "created": 89,
  "success": true
}
```

### GET **`/categories/<int:category_id>/questions`**
Endpoint to get questions based on category
- Request Arguments:
```
/categories/1/questions - category_id - get science questions
/categories/1/questions?page=2 - page (optional)
```
- Returns: An object with all the questions paginated based on the provided category
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "42",
      "category": 1,
      "difficulty": 5,
      "id": 52,
      "question": "What is the answer for the universe and everything else?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### POST **`/quizzes`**
The Endpoint to get questions to play the quiz. This endpoint take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

- Request Arguments:
```
{
	"previous_questions": [1,2,3],
	"quiz_category": {"id": 1, "type": "Science"}
}
```
- Returns: An object with a random question, if is the last question of the category will return `null`
```
{
  "question": {
    "answer": "42",
    "category": 1,
    "difficulty": 5,
    "id": 78,
    "question": "What is the answer for the universe and everything else?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
