import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testFetchItems(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.id0 = itm.insertItem(owner=1, content='hello', filename='testdb.db')
        self.id1 = itm.insertItem(owner=2, content='bonjour', filename='testdb.db')
        self.id2 = itm.insertItem(owner=3, content='ciao', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testLengthMatches(self):
        items = itm.fetchItems(filename = 'testdb.db')
        self.assertEqual(len(items), 3)

    def testItemsAreObjects(self):
        items = itm.fetchItems(filename = 'testdb.db')
        for item in items:
            self.assertEqual(type(item), itm.Item)

    def testOutputIsList(self):
        items = itm.fetchItems(filename = 'testdb.db')
        self.assertEqual(type(items), list)

class TestFetchItemFromId(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.id0 = itm.insertItem(owner=1, content='hello', filename='testdb.db')
        self.id1 = itm.insertItem(owner=2, content='bonjour', filename='testdb.db')
        self.id2 = itm.insertItem(owner=3, content='ciao', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testIsItemObject(self):
        item0 = itm.fetchItemFromId(self.id0, filename='testdb.db')
        item1 = itm.fetchItemFromId(self.id1, filename='testdb.db')
        item2 = itm.fetchItemFromId(self.id2, filename='testdb.db')
        self.assertEqual(type(item0), itm.Item)
        self.assertEqual(type(item1), itm.Item)
        self.assertEqual(type(item2), itm.Item)
    
    def testItemIds(self):
        item0 = itm.fetchItemFromId(self.id0, filename='testdb.db')
        item1 = itm.fetchItemFromId(self.id1, filename='testdb.db')
        item2 = itm.fetchItemFromId(self.id2, filename='testdb.db')
        self.assertEqual(item0.owner, 1)
        self.assertEqual(item1.owner, 2)
        self.assertEqual(item2.owner, 3)

    def testItemOwners(self):
        item0 = itm.fetchItemFromId(self.id0, filename='testdb.db')
        item1 = itm.fetchItemFromId(self.id1, filename='testdb.db')
        item2 = itm.fetchItemFromId(self.id2, filename='testdb.db')
        self.assertEqual(item0.id, self.id0)
        self.assertEqual(item1.id, self.id1)
        self.assertEqual(item2.id, self.id2)
    
    def testItemContents(self):
        item0 = itm.fetchItemFromId(self.id0, filename='testdb.db')
        item1 = itm.fetchItemFromId(self.id1, filename='testdb.db')
        item2 = itm.fetchItemFromId(self.id2, filename='testdb.db')
        self.assertEqual(item0.content, 'hello')
        self.assertEqual(item1.content, 'bonjour')
        self.assertEqual(item2.content, 'ciao')

    def testIsNone(self):
        item0 = itm.fetchItemFromId(433, filename='testdb.db')
        item1 = itm.fetchItemFromId(43435, filename='testdb.db')
        item2 = itm.fetchItemFromId(34, filename='testdb.db')
        self.assertIsNone(item0)
        self.assertIsNone(item1)
        self.assertIsNone(item2)

class testFetchItemsFromIds(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.id0 = itm.insertItem(owner=1, content='hello', filename='testdb.db')
        self.id1 = itm.insertItem(owner=2, content='bonjour', filename='testdb.db')
        self.id2 = itm.insertItem(owner=3, content='ciao', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testOutputIsList(self):
        items = itm.fetchItemCollectionFromIds([self.id0, self.id1, self.id2], filename='testdb.db')
        self.assertEqual(type(items), list)

    def testOutputItemsAreObjects(self):
        items = itm.fetchItemCollectionFromIds([self.id0, self.id1, self.id2], filename='testdb.db')
        for item in items:
            self.assertEqual(type(item), itm.Item)

    def testIdNotInDbEdgeCase(self):
            items = itm.fetchItemCollectionFromIds([self.id0, self.id1, self.id2, 100000, 666], filename='testdb.db')
            self.assertEqual(len(items), 3)


class TestFindProjectWithItemId(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        prj.createProjectTable('testdb.db')

        self.item_id0 = itm.insertItem(owner=1, content='hello', filename='testdb.db')
        self.item_id1 = itm.insertItem(owner=2, content='bonjour', filename='testdb.db')
        self.item_id2 = itm.insertItem(owner=3, content='ciao', filename='testdb.db')
        self.item_id3 = itm.insertItem(owner=3, content='Hola', filename='testdb.db')

        self.project_id0 = prj.insertProject(owner=1, title='Test Project', items=[self.item_id0, self.item_id1], position = 0, filename='testdb.db')
        self.project_id1 = prj.insertProject(owner=2, title='Test Project 2', items=[self.item_id2, self.item_id3], position = 1, filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testExists(self):
        result0 = itm.findProjectWithItemId(item_id=self.item_id0, filename='testdb.db')
        result1 = itm.findProjectWithItemId(item_id=self.item_id1, filename='testdb.db')
        result2 = itm.findProjectWithItemId(item_id=self.item_id2, filename='testdb.db')
        result3 = itm.findProjectWithItemId(item_id=self.item_id3, filename='testdb.db')

        self.assertEqual(result0, self.project_id0)
        self.assertEqual(result1, self.project_id0)
        self.assertEqual(result2, self.project_id1)
        self.assertEqual(result3, self.project_id1)
    
    def testNotExists(self):
        result0 = itm.findProjectWithItemId(item_id=111, filename='testdb.db')
        result1 = itm.findProjectWithItemId(item_id=222, filename='testdb.db')
        result2 = itm.findProjectWithItemId(item_id=333, filename='testdb.db')
        result3 = itm.findProjectWithItemId(item_id=444, filename='testdb.db')

        self.assertIsNone(result0)
        self.assertIsNone(result1)
        self.assertIsNone(result2)
        self.assertIsNone(result3)

if __name__ == '__main__':
    unittest.main()