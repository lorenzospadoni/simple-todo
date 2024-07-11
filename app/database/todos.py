import sqlite3, datetime, json, os
from typing import Union

from database.items import *
from database.projects import *
from database.containers import *


working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

def createTodoTables(filename: str = db_file):
    '''Creates both TodoProjects and TodoItems tables. 
    Takes database filename as argument and passes it to both functions'''
    createItemTable(filename)
    createProjectTable(filename)
    createContainerTable(filename)

def removeTodoTables(filename: str = db_file):
    '''Removes both items and projects tables'''
    dropProjectTable(filename)
    dropItemTable(filename)
    dropContainerTable(filename)



