import sqlite3, datetime, json, os
from typing import Union

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

#TODO: How does this handle Nones?
#TODO:should this skip over them or not?
#TODO: unittest this function
def cleanFetchall(record: list):
    output = []
    for rec in record:
        output.append(rec[0])
    return output

def execQuery(query: str, args: tuple, filename: str = db_file) -> None:
    '''Executes a query, commits and closes the connection. Alsways returns None'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def execLastRowId(query: str, args: tuple, filename: str = db_file) -> Union[int, None]:
    '''Executes a query, commits, closes the connection and returns the last rowid accessed
    by the cursor.'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def execRowcount(query: str, args: tuple, filename: str = db_file) -> int:
    '''Executes a query, commits, closes the connection and returns the amount of records modified
    by the query. If none are modified returns zero (0)'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()
    return cursor.rowcount

#TODO: adjust return type
def execFetchone(query: str, args: tuple, filename: str = db_file) -> Union[tuple, None]:
    '''Executes a query, commits, closes the connection and returns the first record
    matching the query's requirements. If none match returns None'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchone()
    connection.close()
    return result

def execFetchall(query: str, args: tuple, filename: str = db_file) -> Union[tuple, None]:
    '''Executes a query, commits, closes the connection and returns ALL the first record
    matching the query's requirements. If none match returns None'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    connection.close()
    return result