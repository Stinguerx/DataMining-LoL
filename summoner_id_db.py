import csv
import sqlite3

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('matches.db')
cursor = conn.cursor()

# Create a table with two columns: rank and summonerid
cursor.execute('''
    CREATE TABLE IF NOT EXISTS summoners (
        rank TEXT,
        summonerid TEXT
    )
''')

# Specify the CSV file name
csv_file_name = 'summoner_ids.csv'

# Open the CSV file and insert data into the table
with open(csv_file_name, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #next(csv_reader)  # Skip the header row if it exists

    for row in csv_reader:
        rank, summonerid = row
        cursor.execute('INSERT INTO summoners VALUES (?, ?)', (rank, summonerid))

cursor.execute('SELECT COUNT(*) FROM summoners')
count = cursor.fetchone()[0]
print("Summoners found in db:", count)

# Commit changes and close the database connection
conn.commit()
conn.close()
