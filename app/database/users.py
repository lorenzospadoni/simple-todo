import sqlite3, datetime, json
## the | operand support is introduced in python 3.10, Almalinux ships 3.9 by default 
## as such import Union
from typing import Union

class User:
    def __init__(self, id: int, username: str, password: str, date_of_subscription: str, is_active: bool):
        self.id = id
        self.username = username
        self.password = password
        self.date_of_subscription = date_of_subscription
        self.is_active = is_active
        self.is_authenticated = True
        self.is_anonymous = False
    def get_id(self):
        return str(self.id)
    def __repr__(self):
        return f'''[USER]
        id: {self.id}
        username: {self.username}
        password: {self.password}
        date_of_subscription: {self.date_of_subscription}
        is_active: {self.is_active}
        is_authenticated: {self.is_authenticated}
        is_anonymous: {self.is_anonymous}
    '''


def createUserTable(filename: str = 'simple-todo.db'):
    '''CREATEs a new user table if one doesn't exist'''
    query = '''CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    date_of_subscription TEXT,
    is_active BOOLEAN
    )'''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def dropUserTable(filename: str = 'simple-todo.db'):
    '''DROPs the users table'''
    query = ''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def createUserObjectFromRecord(record):
    '''Takes a record as argument and returns a User object'''
    id = record[0]
    username = record[1]
    password = record[2]
    date_of_subscription = record[3]
    is_active = bool(record[4])
    user = User(id, username, password, date_of_subscription, is_active)
    return user

def insertUser(username: str, password: str, is_active: bool, filename = 'simple-todo.db'):
    '''Add a new record into the users table'''
    query = 'INSERT INTO users(username, password, date_of_subscription, is_active) VALUES(?,?,?,?)'
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
    args = (username, password, today, is_active, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def deleteUserFromId(id: int, filename = 'simple-todo.db'):
    '''Deletes a user record whose id matches the given id'''
    query = '''DELETE FROM users WHERE id = (?)'''
    args = (id,)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()

def getUsers(filename:str = 'simple-todo.db') -> list:
    '''Fetches all users from the db'''
    query = 'SELECT * FROM users'
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    users = []
    for record in records:
        user = createUserObjectFromRecord(record)
        users.append(user)
    return users

def getUserFromId(id:int, filename = 'simple-todo.db') -> Union[User, None]:
    '''Fetches from the db the user record whose id matches the given id and returns an User object with
    the record's data'''
    query = '''SELECT * FROM users WHERE id = (?)'''
    args = (id,)
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    user_record = cursor.fetchone()
    user = createUserObjectFromRecord(user_record)
    connection.close()
    return user

def getUserFromUsername(username: str, filename = 'simple-todo.db') -> Union[User, None]:
    '''Fetches the user record whose username matches the given one and returns an User object if found'''
    query = ''
    args = (username, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    user = cursor.fetchone()
    connection.close()
    return user

def checkIfUserPasswordIsCorrect(username: str, password: str, filename = 'simple-todo.db') -> Union[bool, None]:
    '''Checks if there is an user record with the given username and tests its password against the
    given one'''
    user = getUserFromUsername(username, filename)
    if user.password == password:
        return True
    elif user.password != password:
        return False
    else:
        return None