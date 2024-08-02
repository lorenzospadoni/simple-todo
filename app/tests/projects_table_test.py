import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testCreateProjectTable(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable('testdb.db')
        self.connection = sqlite3.connect('testdb.db')
        self.cursor = self.connection.cursor()
    def tearDown(self):
        self.connection.commit() # this shouldn't be here find a better location
        self.connection.close()
        # os.remove('testdb.db')
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testTableCreated(self):
        query = "SELECT name FROM sqlite_master WHERE name = 'projects'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        result = result[0]
        self.assertEqual(result, 'projects')

class testDropProjectTable(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('testdb.db')
        self.cursor = self.connection.cursor()
        itm.createItemTable('testdb.db')
        itm.dropItemTable('testdb.db')

    def tearDown(self):
        self.connection.close()
        # os.remove('testdb.db')
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testItemTableDropped(self):
        query = "SELECT name FROM sqlite_master WHERE name = 'projects'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()