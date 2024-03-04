'''
This script demonstrates the usage of SQLite database in Python.
It creates a table 'data' in the database 'my_database.db' and inserts a record into it.
The record consists of a date, file directory, and a tag.
The script also includes a function to retrieve all the data from the table.
'''

import json
import os
from pathlib import Path
import sqlite3

#
global connection
global cursor
global db_path

db_path = ''
connection = None
cursor = None

def init():
    global connection
    global cursor
    global db_path
    # Path to the database file | {CONFIG} set-up-API
    # db_path = r'.\\app_data\\my_database.db'

    # if not os.path.isdir(r'.\\app_data'):
    #     os.mkdir(r'.\\app_data')

    # db_path = 'my_database.db'
    # Create a connection to the database | {INITIALIZE}
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(e)
        # connect to the default database {when app first initialized}
        init_db_path = os.path.join(Path(os.path.expanduser("~/Documents")), 'TrackMyFiles', 'my_database.db')
        connection = sqlite3.connect(init_db_path)
        cursor = connection.cursor()
        # revert back to the default database {in cconfig.json"}
        config_path = os.path.join(Path(os.path.expanduser("~/Documents")), 'TrackMyFiles', 'config.json')
        config_content = json.load(open(config_path, 'r'))
        config_content['database']['path'] = init_db_path
        json.dump(config_content, open(config_path, 'w'))

    # Create a table in the database | {PREPARE SCHEMA}
    # if not exist, then create again
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY UNIQUE,
            date DATE,
            file_dir TEXT,
            tag TEXT
        )
    """)

# sample data
# date_value = '2021-02-14'
# file_dir_value = 'C:/Users/abc/school.jpg'
# tag_value = 'our school jay roy mila'

def insert_data(date_value:str, file_dir_value:str, tag_value:str) -> None:
    '''
    Inserts a new record into the 'data' table.
    
    Parameters:
    - date_value (str): The date value for the record.
    - file_dir_value (str): The file directory value for the record.
    - tag_value (str): The tag value for the record.
    '''
    global connection
    global cursor
    cursor.execute("""
        INSERT INTO data (date, file_dir, tag) 
        VALUES (?, ?, ?)
    """, (date_value, file_dir_value, tag_value))
    connection.commit()

def get_data_all() -> list:
    '''
    Retrieves all the data from the 'data' table.
    
    Returns:
    - list: A list of tuples representing the records in the table.
    '''
    global cursor

    cursor.execute("""
        SELECT * FROM data
    """)
    return cursor.fetchall()

def update_data(date_value, file_dir_value, new_tag_value):
    global connection
    global cursor
    cursor.execute("""
        UPDATE data 
        SET tag = ? 
        WHERE date = ? AND file_dir = ?
    """, (new_tag_value, date_value, file_dir_value))
    connection.commit()

def delete_data(date_value, file_dir_value) -> None:
    """
    Delete data from the 'data' table based on the given date and file directory.

    Args:
        date_value (str): The date value to match in the 'date' column.
        file_dir_value (str): The file directory value to match in the 'file_dir' column.

    Returns:
        None
    """
    global connection
    global cursor
    cursor.execute("""
        DELETE FROM data 
        WHERE date = ? AND file_dir = ?
    """, (date_value, file_dir_value))
    connection.commit()

def delete_data_by_id(id_value):
    """
    Delete data from the 'data' table based on the given unique id.

    Args:
        id_value (int): The id value to match in the 'id' column.

    Returns:
        None
    """
    global connection
    global cursor
    cursor.execute("""
        DELETE FROM data 
        WHERE id = ?
    """, (id_value,))
    connection.commit()

def search_data_by_tag(tag_value):
    global cursor
    global connection
    cursor.execute("""
        SELECT * FROM data 
        WHERE date = ?
    """, (tag_value,))
    return cursor.fetchall()

def search_data_by_id(id_value):
    global cursor
    global connection
    cursor.execute("""
        SELECT * FROM data 
        WHERE id = ?
    """, (id_value,))
    return cursor.fetchall()

def query_db(query:str) -> list:
    '''
    filter-search
    '''
    # Execute the SQL query
    global cursor
    global connection
    cursor.execute("SELECT * FROM data WHERE tag LIKE '%{}%'".format(query))
    return cursor.fetchall()

def close_db_connection() -> None:
    """
    Closes the database connection and commits any pending changes.

    :return: None
    """
    global connection

    connection.commit()
    connection.close()

# insert_data(date_value, file_dir_value, tag_value)
# print('serachs',search_data('2021-01-21'))
# delete_data_by_id(2)
# init()
# print(query_db('test'))
# [print(x) for x in get_data()]
# close_db_connection()
# print(get_data_all())