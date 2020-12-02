import psycopg2

conn = psycopg2.connect('dbname=app_database user=app_user')

# Open a cursor to perform database operations
cursor = conn.cursor()

# Drop if any TODOS table exist
cursor.execute("DROP TABLE IF EXISTS todos;")

# Create the TODOS table
cursor.execute("""
    CREATE TABLE todos (
        id serial PRIMARY KEY,
        description VARCHAR NOT NULL
    )
""")

# Insert values
cursor.execute('INSERT INTO todos (id, description) VALUES (%s, %s)', (1, 'Frist item test'))

# Inserting others values
SQL = 'INSERT INTO todos (id, description) VALUES (%(id)s, %(description)s);'

data = {
    'id': 2,
    'description': "Second test item"
}
cursor.execute(SQL, data)

# SELECT and fetch all rows created
cursor.execute("SELECT * from todos;")
result = cursor.fetchall()
print(result)

# commit, so it does the executionson the db and persist the modifications
conn.commit()

cursor.close()
conn.close()
