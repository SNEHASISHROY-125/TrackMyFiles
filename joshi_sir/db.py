'''
This script demonstrates the usage of SQLite database in Python.
It creates a table 'data' in the database 'my_database.db' and inserts a record into it.
The record consists of a date, file directory, and a tag.
The script also includes a function to retrieve all the data from the table.
'''

import sqlite3

# Create a connection to the database | {INITIALIZE}
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

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
    cursor.execute("""
        SELECT * FROM data
    """)
    return cursor.fetchall()

def update_data(date_value, file_dir_value, new_tag_value):
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
    cursor.execute("""
        DELETE FROM data 
        WHERE id = ?
    """, (id_value,))
    connection.commit()

def search_data_by_tag(tag_value):
    cursor.execute("""
        SELECT * FROM data 
        WHERE date = ?
    """, (tag_value,))
    return cursor.fetchall()

def search_data_by_id(id_value):
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
    cursor.execute("SELECT * FROM data WHERE tag LIKE '%{}%'".format(query))
    return cursor.fetchall()

def close_db_connection() -> None:
    """
    Closes the database connection and commits any pending changes.

    :return: None
    """
    connection.commit()
    connection.close()

# insert_data(date_value, file_dir_value, tag_value)
# print('serachs',search_data('2021-01-21'))
# delete_data_by_id(4)
# print(query_db('mau5'))
# close_db_connection()
# [print(x) for x in get_data()]
# print(get_data_all())