Fyyur - Edu Version
-----

  Avaliable at: https://github.com/eduduardo/udacity-nanodegree-fullstack/tree/main/02-sql-data-modeling-web/fyyur-project

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Dependencies
- Python3
- Pip
- other dependencies are located on requirements.txt and will be installed on the next steps

## Instructions to run
1. **Create a database on postgres**
2. **Change the connection settings in ``config.py``
```
SQLALCHEMY_DATABASE_URI = 'postgresql://app_user@localhost:5432/fyyur'
```
3. **Initialize and activate a virtualenv using:**
```
python3 -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```
>**Note 2** - if you don't have virtualenv, please install:
```
pip3 install virtualenv
```

4. **Install the dependencies:**
```
python3 -m pip install -r requirements.txt
```

4. **Migrate the tables to postgres**
```
flask db upgrade
```

5. **Run the development server:**
```
python3 app.py
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

7. Enjoy the project!
