import sqlite3, datetime, json

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
    query = ''
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()

def addUser(username: str, password: str, is_active: str, filename = 'simple-todo.db'):
    query = 'INSERT INTO users(username, password, date_of_subscription, is_active) VALUES(?,?,?,?)'
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%s')
    args = (username, password, today, is_active, )
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection.close()