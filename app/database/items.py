import sqlite3, datetime, json, os
from typing import Union

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

def deleteItems(ids: list, filename: str = db_file):
    for id in ids:
        deleteItem(id)

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

def getItemOrder(project_id: int, filename: str = db_file) -> list:
    '''Returns a list of all'''
    query = 'SELECT items FROM projects WHERE id = (?)'
    args = (project_id, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    order = cursor.fetchone()
    connection.close()
    return json.loads(order[0])

def checkIfItemOrderIsSafe():
    pass

def setNewItemOrder(project_id: int, order: list, filename: str = db_file):
    clean_order = []
    for item in order:
        if type(item) == int:
            clean_order.append(item)
        else:
            pass
    print(clean_order)
    query = 'UPDATE projects SET items = (?) WHERE id = (?)'
    args = (json.dumps(clean_order), project_id)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()
    return True


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
