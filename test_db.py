'''
Testing the database connection
'''

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object
cur = conn.cursor()

# Execute the SQL query
cur.execute("SELECT * FROM data WHERE tag LIKE '%pic%'")

# Fetch all the rows
rows = cur.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
