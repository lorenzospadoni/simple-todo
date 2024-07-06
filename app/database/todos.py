import sqlite3, datetime, json, os
from typing import Union

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

class Container(list):
    ## Fix this
    ## The objective of this class is to create an easier centralized way to handle position exchange
    ## between two projects or two items
    
    def __init__(self, *args):
        super().__init__(args)
        self._owner = None
    
    @property
    def owner(self):
        return self._owner
    @owner.setter
    def owner(self, value:int):
        self._owner = value
    @property
    def obj(self):
        return self
    @obj.setter
    def obj(self, projects):
        new_projects = ''
    @property
    def json(self):
        return json.dumps(self.obj)
    @json.setter
    def json(self, value: str):
        cont = json.loads(value)
        self.obj = cont



class Project:
    def __init__(self, id: int, owner: int, title: str, items: list, date_of_creation: str) -> object:
        self.id = id
        self.owner = owner
        self.title = title
        self.items = items
        self.date_of_creation = date_of_creation
    @property
    def obj(self) -> dict:
        children = []
        print(f'THIS IS ITEMS: {self.items} TYPE: {type(self.items)}')
        for item in self.items:
            print('This is Item: ' + str(item))
            children.append(item.obj)
        representation = {
            'title' : self.title,
            'id' : self.id,
            'children' : children
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
class Item:
    def __init__(self, id: int, owner: int, content: str, date_of_creation: str):
        self.id = id
        self.owner = owner
        self.content = content
        self.date_of_creation = date_of_creation
    def __repr__(self):
        return f'''[ITEM]
        id: {self.id}
        owner: {self.owner}
        content: {self.content}
        date_of_creation: {self.date_of_creation}

        '''
    @property
    def obj(self) -> dict:
        representation = {
                'id' : self.id,
                'content' : self.content            
            }
        return representation


def createItemTable(filename: str = db_file ):
    ''' Creates the database table for TodoItems '''
    query = '''
        CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner INTEGER,
        content TEXT,
        date_of_creation TEXT
        );
    '''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def dropItemTable(filename: str = db_file):
    '''Removes the database items table'''
    query = 'DROP TABLE items'
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def createProjectTable(filename: str = db_file):
    ''' Creates the database table for TodoProjects '''
    query = '''
    CREATE TABLE projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER,
    title TEXT,
    items JSON,
    date_of_creation TEXT
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

def createTodoTables(filename: str = db_file):
    '''Creates both TodoProjects and TodoItems tables. 
    Takes database filename as argument and passes it to both functions'''
    createItemTable(filename)
    createProjectTable(filename)

def removeTodoTables(filename: str = db_file):
    '''Removes both items and projects tables'''
    dropProjectTable(filename)
    dropItemTable(filename)

def insertItem(owner: int, content: str, filename: str = db_file) -> Union[int, None]:
    try:
        '''Inserts an item to the database. Datetime is declared by the function'''
        today_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
        query = 'INSERT INTO items(owner, content, date_of_creation) VALUES(?, ?, ?)'
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute(query, (owner, content, today_date))
        row_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return row_id
    except:
        return None

def fromRecordToItem(record: tuple) -> Union[Item, None]:
    '''Converts the output of sqlite to an Item object, returns None if not possible'''
    try:
        id = record[0]
        owner = record[1]
        content = record[2]
        date_of_creation = record[3]
        item = Item(id, owner, content, date_of_creation)
        return item
    except TypeError:
        # TypeError occurs when id = record[0] is not possible because record is of type 'NoneType'
        item = None
    finally:
        return item

def fromRecordsToItemCollection(records: tuple):
    '''Converts the output of sqlite to a collection of Item objects'''
    items = []
    for record in records:
        item = fromRecordToItem(record)
        items.append(item)
    return items

def fetchItems(filename: str = db_file):
    query = '''SELECT * FROM items'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    items_raw = cursor.fetchall()
    items = fromRecordsToItemCollection(items_raw)
    return items

def fetchItemFromId(item_id: int, filename: str = db_file) -> Union[Item, None]:
    '''Returns the item whose id matches the given item id, if none are found returns None'''
    try:
        query = '''SELECT * FROM items WHERE id = (?)'''
        args = (item_id, )
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute(query, args)
        item = fromRecordToItem(cursor.fetchone())
        connection.close()
        return item
    except TypeError:
        return None


def fetchItemCollectionFromIds(ids:list, filename: str = db_file) -> list:
    items = []
    for id in ids:
        item = fetchItemFromId(id, filename)
        items.append(item)
    return items

def updateItemContent(id: int, content: str, filename: str = db_file):
    '''Changes an item's content'''
    query = 'UPDATE items SET content = (?) WHERE id = (?)'
    args = (content, id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def deleteItem(id: int, filename: str = db_file):
    '''Deletes the record of an item whose id matches the given id argument'''
    query = '''DELETE FROM items WHERE id = (?)'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, (id, ))
    connection.commit()
    connection.close()
    return True
def findProjectWithItemId(item_id: int, filename: str = db_file):
    '''Returns the id of the project that has a certain item id in its 'items' field'''
    query = '''
        SELECT projects.id
        FROM projects, json_each(projects.items)
        WHERE json_each.value = (?)
    '''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, (item_id, ))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result[0]

def appendItemToProjectChildren(item_id: int, project_id: int, filename: str = db_file) -> bool:
    '''Appends an Item id to a Project items field in the db '''
    query = '''
        SELECT items FROM projects WHERE id = (?)'''
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    items = json.loads(cursor.fetchone()[0])
    items.append(item_id)
    query = '''
        UPDATE projects SET items = (?) WHERE id=(?)
    '''
    args = (json.dumps(items), project_id)
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def removeItemIdFromProjectItems(item_id: int, project_id: int, filename: str = db_file):
    query = '''
        SELECT items FROM projects WHERE id=(?)
    '''
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    items = cursor.fetchone()
    items = items[0]
    items = json.loads(items)
    items.remove(item_id)
    items = json.dumps(items)
    query = '''
        UPDATE projects SET items = (?) WHERE id = (?)
    '''
    args = (items, project_id)
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def removeItemIdFromProjects(item_id, filename: str = db_file):
    project_id = findProjectWithItemId(item_id, filename)
    removeItemIdFromProjectItems(item_id, project_id, filename)

# Is this bad code?
def userOwnsItem(user_id: int, item_id: int, filename: str = db_file) -> bool:
    '''Checks if a user with a certain user_id is the owner of an item in the db'''
    try:
        item = fetchItemFromId(item_id, filename)
        if item.owner == user_id:
            return True
        else:
            raise AttributeError
    except AttributeError:
        # AttributeError is raised either when you try to access item.owner but fetchItemFromId
        # returned None or when the user is NOT the owner of the Item
        return False
        

def insertProject(owner: int, title:str, items: list, filename: str = db_file) -> Union[int, None]:
    try:
        '''Inserts an item to the database. Datetime is declared by the function'''
        today_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
        query = 'INSERT INTO projects(owner, title, items, date_of_creation) VALUES(?, ?, ?, ?)'
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()
        cursor.execute(query, (owner, title, json.dumps(items), today_date))
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
    items = fetchItemCollectionFromIds(json.loads(record[3]))
    date_of_creation = record[4]
    project = Project(id, owner, title, items, date_of_creation)
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
        item = fromRecordToItem(record)
        items.append(item)
    connection.close()
    return items

def fetchProjects(filename: str = db_file):
    query = '''SELECT * FROM projects'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    projects_raw = cursor.fetchall()
    connection.close()
    projects = []
    for project_raw in projects_raw:
        project = Project(project_raw[0], project_raw[1],project_raw[2],project_raw[3],project_raw[4])
        projects.append(project)
    return projects

def fetchProjectsFromUserId(id:int, filename: str = db_file):
    query = '''SELECT * FROM projects WHERE owner = (?)'''
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


