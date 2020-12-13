# Casting Agency Project
Final project for Udacity Full Stack Developer Nanodegree.

# Motivation
The Casting Agency is a company that is responsible for creating movies and managing and assigning actors to those movies. This project aims to are creating a system to simplify and streamline this process.

# Live project
The live version of this project is hosted on Heroku.
https://edu-casting-agency.herokuapp.com/

### Request Example
```
export DIRECTOR_TOKEN=[ADD_THE_TOKEN_OF_THE_NEXT_STEP]
curl --request GET \
  --url https://edu-casting-agency.herokuapp.com/movies \
  -H "Authorization: Bearer ${DIRECTOR_TOKEN}"
```
```
export ASSISTANT_TOKEN=[ADD_THE_TOKEN_OF_THE_NEXT_STEP]
curl --request GET \
  --url https://edu-casting-agency.herokuapp.com/actors \
  -H "Authorization: Bearer ${ASSISTANT_TOKEN}"
```

### Authentication Steps
There is a file named `tokens.txt` with the 3 users authorization tokens
- Casting Assistant
- Casting Director
- Executive Producer

If the token expires. Please enter on the following link https://dev-ehvlmutg.us.auth0.com/authorize?audience=agency&response_type=token&client_id=0PWzm0kkCTP0sd2T5GJN4lT5fr7Ol8tZ&redirect_uri=https://edu-casting-agency.herokuapp.com/

And login with the credentials:
```
user: assistant@agency.com
pass: agency123456*

user: director@agency.com
pass: agency123456*

user: producer@agency.com
pass: agency123456*
```

Grap the `#access_token=` on the redirected url


# Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

## Database Setup
```bash
CREATE DATABASE casting_agency
psql casting_agency < casting_agency.sql
```

## Running the server

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
export DATABASE_URL=postgresql://app_user@localhost:5432/casting_agency
export AUTH0_DOMAIN=dev-ehvlmutg.us.auth0.com
export AUTH0_AUDIENCE=agency
flask run
```

## Running the tests
To run the tests, first create and testing database or use the created on the first steps
```bash
CREATE DATABASE casting_agency_test
psql casting_agency_test < casting_agency.sql
```

For run the tests:
```bash
export DATABASE_URL_TEST=postgresql://app_user@localhost:5432/casting_agency
export ASSISTANT_TOKEN=
export DIRECTOR_TOKEN=
export PRODUCER_TOKEN=
python test_app.py
```

## API Documentation
#### RBAC
These are all the permissions (scopes) that this API uses.

- `get:actors` - get actors infos
- `create:actors`	- create actor
- `update:actors`	- update actor infos
- `delete:actors`	- delete actor
- `get:movies` - get movies info
- `create:movies`	- create movie
- `update:movies`	- update movie infos
- `delete:movies`	- delete movie

#### Roles Permissions Assignments
- Casting Assistant: [`get:actors`, `get:movies`]
- Casting Director: Assistant permissions + [`create:actors`, `delete:actors`, `update:actors`, `update:movies`]
- Executive Producer: Director + [`delete:movies`, `create:movies`]

#### Endpoints
These are all the endpoints this API dispose:

### GET **`/actors`**
This endpoint return a list of actors, their names, and movies participating, including pagination (every 5)
- Requires: `get:actors`
- Request Arguments:
```
/actors?page=1 (optional) - number of the correspondent page
```
- Returns:
```
{
  "actors": [
    {
      "gender": "male",
      "id": 1,
      "movies": [
        {
          "id": 6,
          "release_date": "1993-12-22",
          "title": "Philadelphia"
        }
      ],
      "name": "Tom Hanks"
    }
  ],
  "success": true,
  "total": 1
}
```

### POST **`/actors`**
This endpoint create an actor according with the arguments passed in the JSON request
- Requires: `create:actors`
- Request Arguments:
```
{
    "name": "Morgan Freeman",
    "gender": "male"
}
```
- Returns:
```
{
  "success": true,
  "actor": 1
}
```

### PATCH **`/actors/<int:actor_id>`**
This endpoint update an actor according with the arguments passed in the JSON request.
This endpoint return if success the actor name and gender,
 otherwise 400 or 422 errors.
- Requires: `update:actors`
- Request Arguments:
```
url: /actors/5
body:
{
    "name": "Morgan Freeman",
    "gender": "male"
}
```
- Returns:
```
{
  "actor": {
    "gender": "male",
    "id": 5
    "name": "Morgan Freeman"
  },
  "success": true
}
```

### DELETE **`/actors/<int:actor_id>`**
Endpoint to DELETE actor using a actor ID
- Requires: `delete:actors`
- Request Arguments:
```
actor_id - actor ID to remove
ex.: /actors/10
```
- Returns: An object with the `deleted` actor ID if success, if not return error.
```
{
  "deleted": 10,
  "success": true
}
```

-----------
### GET **`/movies`**
This endpoint return a list of movies, their title, release_date and actors cast, including pagination (every 5)
- Requires: `get:movies`
- Request Arguments:
```
/movies?page=1 (optional) - number of the correspondent page
```
- Returns:
```
{
  "movies": [
    {
      "actors": [
        {
          "gender": "male",
          "id": 6,
          "name": "Margot Robbie"
        },
        {
          "gender": "male",
          "id": 5,
          "name": "Brad Pitt"
        }
      ],
      "id": 1,
      "release_date": "2020-01-01",
      "title": "Once Upon a Time in Hollywood"
    },
    {
      "actors": [
        {
          "gender": "male",
          "id": 2,
          "name": "Antonio Banderas"
        }
      ],
      "id": 2,
      "release_date": "2019-03-22",
      "title": "Pain and Glory"
    }
  ],
  "success": true,
  "total": 2
}
```

### POST **`/movies`**
This endpoint create a new movie according with the arguments passed in the JSON request, if success the movie ID, otherwise 400 or 422 errors
- Requires: `create:movies`
- Request Arguments:
```
{
    "title": "Pain and Glory",
    "release_date": "2019-03-22"
}
```
- Returns:
```
{
  "success": true,
  "movie": 1
}
```

### PATCH **`/movies/<int:movie_id>`**
This endpoint update a movie according with the arguments passed in the JSON request.
This endpoint return if success the movie title, release_date and cast, otherwise 400 or 422 errors.
- Requires: `update:movies`
- Request Arguments:
```
url: /movies/5
body:
{
    "title": "Pain and Glory",
    "release_date": "2017-12-08"
}
```
- Returns:
```
{
  "movie": {
    "actors": [
      {
        "gender": "male",
        "id": 6,
        "name": "Morgan Freeman"
      }
    ],
    "id": 5,
    "release_date": "2017-12-08",
    "title": "Pain and Glory"
  },
  "success": true
}
```

### DELETE **`/movies/<int:movie_id>`**
Endpoint to DELETE movie using a movie ID
- Requires: `delete:movie`
- Request Arguments:
```
movie_id - movie ID to remove
ex.: /movie/10
```
- Returns: An object with the `deleted` movie ID if success, if not return error.
```
{
  "deleted": 10,
  "success": true
}
```
