import sqlite3, datetime, json, os
from typing import Union

import database.utils as dbutils

working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

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

def testFunction() -> str:
    '''Always returns the string 'hello' '''
    return 'hello'

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
    dbutils.execQuery(query, (), filename)

def dropItemTable(filename: str = db_file):
    '''Removes the database items table'''
    query = 'DROP TABLE items'
    dbutils.execQuery(query, (), filename)


def insertItem(owner: int, content: str, filename: str = db_file) -> Union[int, None]:
    '''Inserts an item to the database. Datetime is declared by the function'''
    today_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
    query = 'INSERT INTO items(owner, content, date_of_creation) VALUES(?, ?, ?)'
    row_id = dbutils.execLastRowId(query, (owner, content, today_date), filename)
    return row_id

def itemExists(item_id: int, filename: str = db_file) -> bool:
    '''Returns True if the given item_id exists in the items table, returns False if it does not'''
    query = 'SELECT * FROM items WHERE id = (?)'
    args = (item_id, )
    item = dbutils.execFetchone(query, args, filename)
    if item != None:
        return True
    else:
        return False

def fromRecordToItem(record: tuple) -> Union[Item, None]:
    '''Converts the output of sqlite to an Item object, returns None if not possible'''
    try:
        id = record[0]
        owner = record[1]
        content = record[2]
        date_of_creation = record[3]
        item = Item(id, owner, content, date_of_creation)
        return item
    except (TypeError, IndexError):
        # TypeError occurs when id = record[0] is not possible because record is of type 'NoneType'
        return None

def fromRecordsToItemCollection(records: tuple) -> list:
    '''Converts the output of sqlite to a collection of Item objects'''
    items = []
    try:
        for record in records:
            if record != None:
                item = fromRecordToItem(record)
                items.append(item)
            else:
                pass
        return items
    except TypeError:
        return list()

def fetchItems(filename: str = db_file) -> list:
    '''Returns a list containing all the items in the db'''
    query = '''SELECT * FROM items'''
    items_raw = dbutils.execFetchall(query, (), filename)
    items = fromRecordsToItemCollection(items_raw)
    return items

def fetchItemFromId(item_id: int, filename: str = db_file) -> Union[Item, None]:
    '''Returns the item whose id matches the given item id, if none are found returns None'''
    try:
        query = '''SELECT * FROM items WHERE id = (?)'''
        args = (item_id, )
        item_raw = dbutils.execFetchone(query, args, filename)
        item = fromRecordToItem(item_raw)
        return item
    except TypeError:
        return None

def fetchItemIdCollectionFromProjectId(project_id: int, filename: str = db_file):
    query = 'SELECT items FROM projects WHERE id = (?)'
    args = (project_id, )
    items = dbutils.execFetchone(query, args, filename)
    items = items[0]
    items = json.loads(items)
    return items

def fetchItemCollectionFromIds(item_ids: list, filename: str = db_file) -> list:
    items = []
    for item_id in item_ids:
        item = fetchItemFromId(item_id, filename)
        if item != None:
            items.append(item)
        else:
            continue
    return items

def updateItemContent(item_id: int, content: str, filename: str = db_file) -> bool:
    '''Changes an item's content, returns True if the update was successful and False if it was not'''
    query = 'UPDATE items SET content = (?) WHERE id = (?)'
    args = (content, item_id)
    rowcount = dbutils.execRowcount(query, args, filename)
    success = rowcount > 0
    return success

def deleteItem(item_id: int, filename: str = db_file):
    '''Deletes the record of an item whose id matches the given id argument, 
    returns True if a row was affected, False if it was not'''
    query = '''DELETE FROM items WHERE id = (?)'''
    args = (item_id, )
    rowcount = dbutils.execRowcount(query, args, filename)
    success = rowcount > 0
    return success

def deleteItems(item_ids: list, filename: str = db_file):
    for item_id in item_ids:
        deleteItem(item_id, filename)

def findProjectWithItemId(item_id: int, filename: str = db_file) -> Union[int, None]:
    #TODO: move this to projects
    try:
        '''Returns the id of the project that has a certain item id in its 'items' field'''
        query = '''
            SELECT projects.id
            FROM projects, json_each(projects.items)
            WHERE json_each.value = (?)
        '''
        args = (item_id, )
        result = dbutils.execFetchone(query, args, filename)
        project = result[0]
        return project
    except TypeError:
        return None

#TODO: move this to projects (maybe?)
def appendItemToProjectChildren(item_id: int, project_id: int, filename: str = db_file) -> bool:
    '''Appends an Item id to a Project items field in the db '''
    try:
        query = '''
            SELECT items FROM projects WHERE id = (?)'''
        args = (project_id, )

        result = dbutils.execFetchone(query, args, filename)
        item_ids = json.loads(result[0])
        item_ids.append(item_id)

        query = '''
            UPDATE projects SET items = (?) WHERE id=(?)
        '''
        args = (json.dumps(item_ids), project_id)

        rowcount = dbutils.execRowcount(query, args, filename)
        success = rowcount > 0
        return success
    except TypeError:
        # this happens when result is None in json.loads(result[0])
        return False


#TODO: this doesn't have error handling??? 
def getItemOrder(project_id: int, filename: str = db_file) -> list:
    '''Returns a list of all the items belonging toa project'''
    query = 'SELECT items FROM projects WHERE id = (?)'
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    result = dbutils.execFetchone(query, args, filename)
    order_json = result[0]
    order = json.loads(order_json)
    return order

#TODO: finish all validations
def checkIfItemOrderIsSafe():
    pass

#TODO: this doesn't seem to return wether the UPDATE was successful or not
def setNewItemOrder(project_id: int, order: list, filename: str = db_file):
    clean_order = []
    for item in order:
        if type(item) == int:
            clean_order.append(item)
        else:
            pass
    query = 'UPDATE projects SET items = (?) WHERE id = (?)'
    args = (json.dumps(clean_order), project_id)
    rowcount = dbutils.execRowcount(query, args, filename)
    success = rowcount > 0
    return success


def removeItemIdFromProjectItems(item_id: int, project_id: int, filename: str = db_file) -> bool:
    query = '''
        SELECT items FROM projects WHERE id=(?)
    '''
    args = (project_id, )
    result = dbutils.execFetchone(query, args, filename)
    items = result[0]
    items = json.loads(items)
    items.remove(item_id)
    items = json.dumps(items)
    query = '''
        UPDATE projects SET items = (?) WHERE id = (?)
    '''
    args = (items, project_id)
    rowcount = dbutils.execRowcount(query, args, filename)
    success = rowcount > 0
    return success


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
    
def userOwnsItems(user_id: int, item_ids: list, filename: str = db_file) -> bool:
    result = None
    for item_id in item_ids:
        iter_result = userOwnsItem(user_id, item_id, filename)
        if iter_result == False:
            result = False
            return result
        elif iter_result == True:
            pass
    result = True
    return result   
