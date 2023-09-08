import sqlite3

# Create or connect to the database (if it doesn't exist, it will be created)
connection = sqlite3.connect('matches.db')

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create a table to store match IDs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS match (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT NOT NULL UNIQUE
    )
''')

# Commit the changes and close the database connection
connection.commit()
connection.close()