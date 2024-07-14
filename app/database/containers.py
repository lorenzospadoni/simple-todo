import sqlite3, datetime, json, os
from typing import Union

#from projects import fetchProjectsFromIds

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

class Container():
    ## Fix this
    ## The objective of this class is to create an easier centralized way to handle position exchange
    ## between two projects or two items
    def __init__(self, id: int, owner: int, _projects:list):
        self.id = id
        self.owner = owner
        self._projects = _projects
    
    def __repr__(self):
        return f'''[CONTAINER]
        Id : { self.id }
        Owner : { self.owner }
        Projects : { self._projects }
        '''

def createContainerTable(filename: str = db_file):
    query = '''CREATE TABLE containers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner INTEGER,
        projects JSON
        )'''
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

def insertContainer(owner:int, projects:list, filename: str = db_file) -> Union[int, None]:
    query = 'INSERT INTO containers(owner, projects) VALUES (?, ?)'
    args = (owner, json.dumps(projects))
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    last_row = cursor.lastrowid
    connection.commit()
    connection.close()
    return last_row

def deleteContainer(rowid:int, filename: str = db_file):
    query = 'DELETE FROM containers WHERE id = (?)'
    args = (rowid, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    last_row = cursor.lastrowid
    connection.commit()
    connection.close()
    return last_row

def deleteContainerFromUserId(user_id: int, filename: str = db_file):
    query = 'DELETE FROM containers WHERE owner = (?)'
    args = (user_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    last_row = cursor.lastrowid
    connection.commit()
    connection.close()
    return last_row

def fetchContainers(filename: str = db_file):
    query = 'SELECT * FROM containers'
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    containers = cursor.fetchall()
    connection.commit()
    connection.close()
    return containers

def fetchContainerFromId(container_id:int, filename: str = db_file):
    query = 'SELECT * FROM containers WHERE id=(?)'
    args = (container_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    container = cursor.fetchone()
    connection.commit()
    connection.close()
    return container

def fetchContainerFromUserId(user_id:int, filename: str = db_file):
    query = 'SELECT * FROM containers WHERE owner=(?)'
    args = (user_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    container = cursor.fetchone()
    connection.commit()
    connection.close()
    return container

def fromRecordToContainer(record):
    rowid = record[0]
    owner = record[1]
    projects = json.loads(record[2])
    container = Container(rowid, owner, projects)
    return container

def fromRecordsToContainers(records):
    containers = []
    for record in records:
        new_record = fromRecordToContainer(record)
        containers.append(new_record)
    return containers

def addProjectToContainer(container_id: int, project_id: int, filename: str = db_file):
    container = fromRecordToContainer(fetchContainerFromId(container_id))
    projects = container.projects
    projects.append(project_id)
    projects = json.dumps(projects)
    query = 'UPDATE containers SET projects = (?) WHERE id = (?)'
    args = (projects, container_id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()
    return True