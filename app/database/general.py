import sqlite3, os

def removeDatabase(filename: str = 'simple-todo.db'):
    print('[general.py: removeDatabase] deleting database')
    os.remove(filename)

def createDatabase(filename: str = 'simple-todo.db'):
    print('[general.py: createDatabase] creating database')
    connection = sqlite3.connect(filename)
    connection.close()


