import sqlite3, datetime, json, os, sys
from typing import Union

myenv = sys.path

import database.items as dbitems

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

class Project:
    def __init__(self, id: int, owner: int, title: str, items: list, date_of_creation: str, position) -> object:
        self.id = id
        self.owner = owner
        self.title = title
        self.items = items
        self.date_of_creation = date_of_creation
        self.position = position
    @property
    def obj(self) -> dict:
        children = []
        #print(f'THIS IS ITEMS: {self.items} TYPE: {type(self.items)}')
        for item in self.items:
            #print('This is Item: ' + str(item))
            children.append(item.obj)
        representation = {
            'title' : self.title,
            'id' : self.id,
            'children' : children,
            'position' : self.position
        }
        return representation
    @property
    def item_list(self) -> list:
        pass
    @staticmethod
    def fetchItemObjects(ids: list, filename: str = db_file):
        query = 'SELECT * FROM items WHERE id = (?)'
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        items = []
        for id in ids:
            cursor.execute(query, (id, ))
            item = cursor.fetchone()
            items.append(item)
        connection.close()
        return items
    def __repr__(self):
        return f'''[PROJECT]
        id: {self.id}
        owner: {self.owner}
        title: {self.title}
        items: {self.items}
        date_of_creation: {self.date_of_creation}
        '''
    
def createProjectTable(filename: str = db_file):
    ''' Creates the database table for TodoProjects '''
    query = '''
    CREATE TABLE projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER,
    title TEXT,
    items JSON,
    date_of_creation TEXT,
    position INTEGER
    );
    '''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def dropProjectTable(filename: str = db_file):
    '''Removes the database project table'''
    query = 'DROP TABLE projects'
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def insertProject(owner: int, title:str, items: list, position: int,filename: str = db_file) -> Union[int, None]:
    try:
        '''Inserts a project to the database. Datetime is declared by the function'''
        today_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
        query = 'INSERT INTO projects(owner, title, items, date_of_creation, position) VALUES(?, ?, ?, ?, ?)'
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute(query, (owner, title, json.dumps(items), today_date, position))
        last_row = cursor.lastrowid
        connection.commit()
        connection.close()
        return last_row
    except:
        return None

def updateProjectTitle(project_id: int, new_title: str, filename: str = db_file):
    '''Updates the title of the project matching the given project id'''
    query = 'UPDATE projects SET title = (?) WHERE id = (?)'
    args = (new_title, project_id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def convertProjectCollectionToList(projects: list):
    coll = []
    try:
        for project in projects:
            coll_json = project.obj
            coll.append(coll_json)
    except AttributeError:
        pass
    return coll

def fromRecordToProject(record: tuple) -> Project:
    '''Returns a Project object from sqlite output'''
    id = record[0]
    owner = record[1]
    title = record[2]
    items = dbitems.fetchItemCollectionFromIds(json.loads(record[3]))
    date_of_creation = record[4]
    position = record[5]
    project = Project(id, owner, title, items, date_of_creation, position)
    return project

def fromRecordsToProjectCollection(records: tuple) -> list:
    '''Returns a Project collection from sqlite output'''
    projects = []
    for record in records:
        project = fromRecordToProject(record)
        projects.append(project)
    return projects

def fetchProjectFromProjectId(project_id: int, filename: str = db_file) -> Union[int, None]:
    '''Returns the project with the given id, returns None if none are found'''
    query = 'SELECT * FROM projects WHERE id = (?)'
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    record = cursor.fetchone()
    #return record[3]
    project = fromRecordToProject(record)
    connection.close()
    return project

def fetchProjectItems(project_id: int, owner_id:int, filename: str = db_file):
    '''Returns all the items belonging to a project where the owner is the given's user'''
    query = '''SELECT items FROM projects WHERE id = (?) AND owner = (?)'''
    args = (project_id, owner_id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    item_ids = cursor.fetchone()
    item_ids = item_ids[0]
    item_ids = json.loads(item_ids)
    # print(type(item_ids[0]))
    items = []
    for item_id in item_ids:
        cursor.execute('SELECT * FROM items WHERE id = (?)', (item_id,))
        record = cursor.fetchone()
        item = dbitems.fromRecordToItem(record)
        items.append(item)
    connection.close()
    return items

def fetchProjects(filename: str = db_file):
    query = '''SELECT * FROM projects ORDER BY position ASC'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    projects_raw = cursor.fetchall()
    connection.close()
    # projects = []
    projects = fromRecordsToProjectCollection(projects_raw)
    return projects

def fetchProjectsFromUserId(id:int, filename: str = db_file):
    query = '''SELECT * FROM projects WHERE owner = (?) ORDER BY position ASC'''
    args = (id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    projects_raw = cursor.fetchall()
    connection.close()
    projects = fromRecordsToProjectCollection(projects_raw)
    #print(projects)
    return projects

def deleteProject(id, filename: str = db_file):
    '''Deletes the record of a project whose id matches the given id argument'''
    query = '''DELETE FROM projects WHERE id = (?)'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, (id, ))
    connection.commit()
    connection.close()

def deleteProjectItems(project_id, filename: str = db_file):
    query = 'SELECT items FROM projects WHERE id = (?)'
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    items = cursor.fetchone()
    items = json.loads(items[0])
    dbitems.deleteItems(items)
    connection.commit()
    connection.close()
    return True

def userOwnsProject(user_id:int, project_id:int, filename: str = db_file):
    '''Checks if a user with a certain user_id is the owner of a project in the db'''
    try:
        project = fetchProjectFromProjectId(project_id, filename)
        if project.owner == user_id:
            return True
        else:
            raise AttributeError
    except AttributeError:
        # AttributeError is raised either when you try to access project.owner but fetchProjectFromProjectId
        # returned None or when the user is NOT the owner of the Project
        return False

def userOwnsProjects(user_id:int, project_ids: list, filename: str = db_file):
    '''Checks if a user with a certain user_id is the owner of all the given projects'''
    for project_id in project_ids:
        success = userOwnsProject(user_id, project_id)
        if success == True:
            pass
        elif success == False:
            return False
    return True

def getBiggestPosition(user_id: int, filename: str = db_file) -> int:
    query = 'SELECT MAX(position) FROM projects WHERE owner = (?)'
    args = (user_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    position = cursor.fetchone()
    position = position[0]
    if position != None:
        return position
    else:
        return 0


def updateProjectPosition(project_id: int, position: int, filename: str = db_file):
    query = 'UPDATE projects SET position = (?) WHERE id = (?)'
    args = (position, project_id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()


