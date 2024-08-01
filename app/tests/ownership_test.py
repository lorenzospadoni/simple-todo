import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class TestUserOwnsItem(unittest.TestCase):
    def setUp(self):
        itm.createItemTable(filename='testdb.db')
        self.item0 = itm.insertItem(owner = 1, content='ciao', filename='testdb.db')
        self.item1 = itm.insertItem(owner = 2, content='hello', filename='testdb.db')
        self.item2 = itm.insertItem(owner = 3, content='bonjour', filename='testdb.db')
        self.item3 = itm.insertItem(owner = 4, content='hola', filename='testdb.db')
               
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testTrue(self):
        result0 = itm.userOwnsItem(user_id = 1, item_id = self.item0, filename='testdb.db')
        result1 = itm.userOwnsItem(user_id = 2, item_id = self.item1, filename='testdb.db')
        result2 = itm.userOwnsItem(user_id = 3, item_id = self.item2, filename='testdb.db')
        result3 = itm.userOwnsItem(user_id = 4, item_id = self.item3, filename='testdb.db')
        results = [result0, result1, result2, result3]

        for result in results:
            self.assertTrue(result)

    def testFalse(self):
        result0 = itm.userOwnsItem(user_id = 555, item_id = self.item0, filename='testdb.db')
        result1 = itm.userOwnsItem(user_id = 8785, item_id = self.item1, filename='testdb.db')
        result2 = itm.userOwnsItem(user_id = 32345, item_id = self.item2, filename='testdb.db')
        result3 = itm.userOwnsItem(user_id = 35342, item_id = self.item3, filename='testdb.db')
        results = [result0, result1, result2, result3]

        for result in results:
            self.assertFalse(result)

    def testItemNotExists(self):
        result0 = itm.userOwnsItem(user_id = 555, item_id = 3463, filename='testdb.db')
        result1 = itm.userOwnsItem(user_id = 8785, item_id = 3463, filename='testdb.db')
        result2 = itm.userOwnsItem(user_id = 32345, item_id = 6565, filename='testdb.db')
        result3 = itm.userOwnsItem(user_id = 35342, item_id = 11, filename='testdb.db')
        results = [result0, result1, result2, result3]

        for result in results:
            self.assertFalse(result)

class TestUserOwnsItems(unittest.TestCase):
    def setUp(self):
        itm.createItemTable(filename='testdb.db')
        self.item0 = itm.insertItem(owner = 1, content='ciao', filename='testdb.db')
        self.item1 = itm.insertItem(owner = 1, content='hello', filename='testdb.db')
        self.item2 = itm.insertItem(owner = 2, content='bonjour', filename='testdb.db')
        self.item3 = itm.insertItem(owner = 2, content='hola', filename='testdb.db')
               
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testTrue(self):
        result0 = itm.userOwnsItems(user_id=1, item_ids=[self.item0, self.item1], filename='testdb.db')
        result1 = itm.userOwnsItems(user_id=1, item_ids=[self.item0, self.item1], filename='testdb.db')

        results = [result0, result1]

        for result in results:
            self.assertTrue(result)

    def testFalse(self):
        result0 = itm.userOwnsItems(user_id = 555, item_ids = [self.item0, self.item1], filename='testdb.db')
        result1 = itm.userOwnsItems(user_id = 8785, item_ids = [self.item2, self.item3], filename='testdb.db')
        result2 = itm.userOwnsItems(user_id = 32345, item_ids = [self.item0, self.item3], filename='testdb.db')
        result3 = itm.userOwnsItems(user_id = 35342, item_ids = [self.item1, self.item2], filename='testdb.db')
        results = [result0, result1, result2, result3]

        for result in results:
            self.assertFalse(result)

    def testItemNotExists(self):
        result0 = itm.userOwnsItems(user_id = 555, item_ids = [3463, 43], filename='testdb.db')
        result1 = itm.userOwnsItems(user_id = 8785, item_ids = [3463, 54353], filename='testdb.db')
        result2 = itm.userOwnsItems(user_id = 32345, item_ids = [6565, 1], filename='testdb.db')
        result3 = itm.userOwnsItems(user_id = 35342, item_ids = [11, 56], filename='testdb.db')
        results = [result0, result1, result2, result3]

        for result in results:
            self.assertFalse(result)
            