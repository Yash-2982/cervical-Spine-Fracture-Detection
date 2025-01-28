import sqlite3

# Connect to the database (creates a new database file if it doesn't exist)
conn = sqlite3.connect('user_database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Execute an SQL command to create a table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
