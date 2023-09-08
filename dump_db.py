import time
import sqlite3
import csv

connection = sqlite3.connect('matches.db')
cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM match')
count = cursor.fetchone()[0]
print("Matches found in db:", count)

cursor.execute('SELECT * FROM match')
rows = cursor.fetchall()

csv_file_name = 'matches.csv'

with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    column_names = [description[0] for description in cursor.description]
    csv_writer.writerow(column_names)
    csv_writer.writerows(rows)     

connection.close()