import sqlite3, datetime, json, os
from typing import Union

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

class Container():
    ## Fix this
    ## The objective of this class is to create an easier centralized way to handle position exchange
    ## between two projects or two items
    def __init__(self, owner, _items):
        self.owner = owner
        self._items = _items

def createContainerTable(filename: str = db_file):
    query = '''CREATE TABLE containers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner INTEGER,
        projects JSON'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def dropContainerTable(filename: str = db_file):
    query = 'DROP TABLE containers'
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()