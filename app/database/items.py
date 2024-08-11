import sqlite3, datetime, json, os
from typing import Union

import database.utils as dbutils
working_directory = os.path.dirname(__file__)
db_file = working_directory + '/' + 'simple-todo.db'

class Item:
    def __init__(self, id: int, owner: int, parent: int, position: int, content: str, date_of_creation: str):
        self.id = id
        self.owner = owner
        self.parent = parent
        self.position = position
        self.content = content
        self.date_of_creation = date_of_creation
    def __repr__(self):
        return f'''[ITEM]
        id: {self.id}
        owner: {self.owner}
        parent: {self.parent}
        position: {self.position}
        content: {self.content}
        date_of_creation: {self.date_of_creation}

        '''
    @property
    def obj(self) -> dict:
        representation = {
                'id' : self.id,
                'parent' : self.parent,
                'position' : self.position,
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
        parent INTEGER,
        position INTEGER,
        content TEXT,
        date_of_creation TEXT
        );
    '''
    dbutils.execQuery(query, (), filename)

def dropItemTable(filename: str = db_file):
    '''Removes the database items table'''
    query = 'DROP TABLE items'
    dbutils.execQuery(query, (), filename)


def insertItem(owner: int, parent: int, position: int, content: str, filename: str = db_file) -> Union[int, None]:
    '''Inserts an item to the database. Datetime is declared by the function. 
    If the record is created returns the id, otherwise returns None'''
    today_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
    query = 'INSERT INTO items(owner, parent, position, content, date_of_creation) VALUES(?, ?, ?, ?, ?)'
    args = (owner, parent, position, content, today_date)
    row_id = dbutils.execLastRowId(query, args, filename)
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
        parent = record[2]
        position = record[3]
        content = record[4]
        date_of_creation = record[5]
        item = Item(id, owner, parent, position, content, date_of_creation)
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
    query = '''SELECT * FROM items ORDER BY position ASC'''
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

#TODO: is this tested?
def fetchItemIdCollectionFromProjectId(project_id: int, filename: str = db_file) -> list:
    query = 'SELECT id FROM items WHERE parent = (?)'
    args = (project_id, )
    items = dbutils.execFetchall(query, args, filename)
    items = list(items)
    return items

#TODO: Test this
def fetchItemCollectionFromProjectId(project_id: int, filename: str = db_file) -> list:
    query = 'SELECT * FROM items WHERE parent = (?) ORDER BY position'
    args = (project_id, )
    result = dbutils.execFetchall(query, args, filename)
    items = fromRecordsToItemCollection(result)
    if items == None:
        items = []
    print(items)
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
            SELECT parent FROM items WHERE id=(?)
'''
        # query = '''
        #     SELECT projects.id
        #     FROM projects, json_each(projects.items)
        #     WHERE json_each.value = (?)
        # '''
        args = (item_id, )
        result = dbutils.execFetchone(query, args, filename)
        project = result[0]
        return project
    except TypeError:
        return None

#TODO: unittest this function
def getItemGreatestPosition(project_id: int, filename: str = db_file) -> Union[int, None]:
    '''Returns the greatest position taken amongst all the items belonging to a project'''
    # TODO: should I worry about user ownership?
    query = 'SELECT MAX(position) FROM items WHERE parent=(?)'
    args = (project_id, )
    result = dbutils.execFetchone(query, args, filename)
    position = result[0]
    if position == None:
        position = 0
    return position


#TODO: this doesn't have error handling??? 
def getItemOrder(project_id: int, filename: str = db_file) -> list:
    '''Returns a list of all the items belonging to a project'''
    query = 'SELECT id FROM items WHERE parent = (?)'
    args = (project_id, )
    result = dbutils.execFetchall(query, args, filename)
    order = []
    for res in result:
        order.append(res[0])
    if result == None:
        return list()
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
    # ensures the item id is valid
    query = 'UPDATE items SET position = (?) WHERE id = (?)'
    args = (json.dumps(clean_order), project_id)
    counter = 0
    successes = []
    for item_id in clean_order:
        counter = counter + 1
        args = (counter, item_id)
        rowcount = dbutils.execRowcount(query, args, filename)
        success = rowcount > 0
        successes.append(success)

    # if any of the results is fallacious returns False
    for succ in successes:
        if succ == True:
            success = True
        else:
            return False
    return success

# DEPRECATED
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
