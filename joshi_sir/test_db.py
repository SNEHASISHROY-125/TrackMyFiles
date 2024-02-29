'''
Testing the database connection
'''

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Create a cursor object
cur = conn.cursor()

def query_db(query:str) -> list:
    #  Execute the SQL query
    cur.execute("SELECT * FROM data WHERE tag LIKE '%{}%'".format(query))
    return cur.fetchall()

# Fetch all the rows
# print(_:=query_db('jay'))
# rows = _
# print((rows[-1][-2]))

# # Print the rows
# for row in rows:
#     print(row)

# Close the connection
# conn.close()
