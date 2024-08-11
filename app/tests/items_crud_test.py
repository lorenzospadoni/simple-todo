import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testInsertItem(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.a_id = itm.insertItem(owner=1, parent = 1, position=1, content='hello', filename='testdb.db')
        self.b_id = itm.insertItem(owner=2, parent = 1, position=2, content='bonjour', filename='testdb.db')
        self.c_id = itm.insertItem(owner=3, parent = 1, position=3, content='ciao', filename='testdb.db')
        self.items = itm.fetchItems('testdb.db')
        self.a_item = self.items[0]
        self.b_item = self.items[1]
        self.c_item = self.items[2]



    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testItemsLength(self):
        self.assertEqual(len(self.items), 3)

    def testItemIdMatches(self):
        self.assertEqual(self.a_id, self.a_item.id)
        self.assertEqual(self.b_id, self.b_item.id)
        self.assertEqual(self.c_id, self.c_item.id)
    
    def testOutputIsList(self):
        self.assertEqual(type(self.items), list)

    def testOutputMembersAreItems(self):
        self.assertEqual(type(self.a_item), itm.Item)
        self.assertEqual(type(self.b_item), itm.Item)
        self.assertEqual(type(self.c_item), itm.Item)

class testItemExists(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.a_id = itm.insertItem(owner=1, parent=0, position = 0, content='hello', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testTrue(self):
        result = itm.itemExists(self.a_id, filename='testdb.db')
        self.assertTrue(result)

    def testFalse(self):
        result = itm.itemExists(1000, filename='testdb.db')
        self.assertFalse(result)

    def testInvalid(self):
        pass

    #TODO: should this handle invalid requests as False?


class TestUpdateItemContent(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.id0 = itm.insertItem(owner=1, parent = 1, position=1, content='hello', filename='testdb.db')
        self.id1 = itm.insertItem(owner=2, parent = 1, position=2, content='bonjour', filename='testdb.db')
        self.id2 = itm.insertItem(owner=3, parent = 1, position=3, content='ciao', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testIfItemExistsTrue(self):
        result0 = itm.updateItemContent(self.id0, 'olleh', filename='testdb.db')
        result1 = itm.updateItemContent(self.id1, 'ruojnob', filename='testdb.db')
        result2 = itm.updateItemContent(self.id2, 'oaic', filename='testdb.db')
        self.assertTrue(result0)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def testIfItemNotExistsFalse(self):
        result0 = itm.updateItemContent(34, 'olleh', filename='testdb.db')
        result1 = itm.updateItemContent(22, 'ruojnob', filename='testdb.db')
        result2 = itm.updateItemContent(7, 'oaic', filename='testdb.db')
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertFalse(result2)

    def testIfContentIsChanged(self):
        result0 = itm.updateItemContent(self.id0, 'olleh', filename='testdb.db')
        result1 = itm.updateItemContent(self.id1, 'ruojnob', filename='testdb.db')
        result2 = itm.updateItemContent(self.id2, 'oaic', filename='testdb.db')
        items = itm.fetchItemCollectionFromIds([self.id0, self.id1, self.id2], filename='testdb.db')
        self.assertEqual(items[0].content, 'olleh')
        self.assertEqual(items[1].content, 'ruojnob')
        self.assertEqual(items[2].content, 'oaic')

class TestDeleteItem(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.id0 = itm.insertItem(owner=1, parent = 1, position=1, content='hello', filename='testdb.db')
        self.id1 = itm.insertItem(owner=2, parent = 1, position=1, content='bonjour', filename='testdb.db')
        self.id2 = itm.insertItem(owner=3, parent = 1, position=1, content='ciao', filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testItemLength(self):
        itm.deleteItem(self.id0, 'testdb.db')
        items = itm.fetchItems('testdb.db')
        self.assertEqual(len(items), 2)

        itm.deleteItem(self.id1, 'testdb.db')
        items = itm.fetchItems('testdb.db')
        self.assertEqual(len(items), 1)

        itm.deleteItem(self.id2, 'testdb.db')
        items = itm.fetchItems('testdb.db')
        self.assertEqual(len(items), 0)

    def testIfItemExistsTrue(self):
        result0 = itm.deleteItem(self.id0, 'testdb.db')
        result1 = itm.deleteItem(self.id1, 'testdb.db')
        result2 = itm.deleteItem(self.id2, 'testdb.db')
        self.assertTrue(result0)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def testIfItemNotExistsFalse(self):
        result0 = itm.deleteItem(1000, 'testdb.db')
        result1 = itm.deleteItem(100, 'testdb.db')
        result2 = itm.deleteItem(44, 'testdb.db')
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertFalse(result2)
    
    def testDeletionRemovesId(self):
        itm.deleteItem(self.id0, 'testdb.db')
        item0 = itm.fetchItemFromId(self.id0, 'testdb.db')
        self.assertIsNone(item0)

        itm.deleteItem(self.id1, 'testdb.db')
        item1 = itm.fetchItemFromId(self.id1, 'testdb.db')
        self.assertIsNone(item1)

        itm.deleteItem(self.id2, 'testdb.db')
        item2 = itm.fetchItemFromId(self.id2, 'testdb.db')
        self.assertIsNone(item2)

##TODO: finish developing TestDeleteItems
# class TestDeleteItems(unittest.TestCase):
#     def setUp(self):
#         itm.createItemTable('testdb.db')
#         self.id0 = itm.insertItem(owner=1, content='hello', filename='testdb.db')
#         self.id1 = itm.insertItem(owner=2, content='bonjour', filename='testdb.db')
#         self.id2 = itm.insertItem(owner=3, content='ciao', filename='testdb.db')

#     def tearDown(self):
#         if os.path.exists('testdb.db') == True:
#             os.remove('testdb.db')
#         else:
#             raise FileNotFoundError('testdb.db does not seem to exist')
    
#     def testItemLength(self):
#         itm.deleteItem(self.id0, 'testdb.db')
#         items = itm.fetchItems('testdb.db')
#         self.assertEqual(len(items), 2)

#         itm.deleteItem(self.id1, 'testdb.db')
#         items = itm.fetchItems('testdb.db')
#         self.assertEqual(len(items), 1)

#         itm.deleteItem(self.id2, 'testdb.db')
#         items = itm.fetchItems('testdb.db')
#         self.assertEqual(len(items), 0)

#     def testIfItemExistsTrue(self):
#         result0 = itm.deleteItem(self.id0, 'testdb.db')
#         result1 = itm.deleteItem(self.id1, 'testdb.db')
#         result2 = itm.deleteItem(self.id2, 'testdb.db')
#         self.assertTrue(result0)
#         self.assertTrue(result1)
#         self.assertTrue(result2)

#     def testIfItemNotExistsFalse(self):
#         result0 = itm.deleteItem(1000, 'testdb.db')
#         result1 = itm.deleteItem(100, 'testdb.db')
#         result2 = itm.deleteItem(44, 'testdb.db')
#         self.assertFalse(result0)
#         self.assertFalse(result1)
#         self.assertFalse(result2)
    
#     def testDeletionRemovesId(self):
#         itm.deleteItem(self.id0, 'testdb.db')
#         item0 = itm.fetchItemFromId(self.id0, 'testdb.db')
#         self.assertIsNone(item0)

#         itm.deleteItem(self.id1, 'testdb.db')
#         item1 = itm.fetchItemFromId(self.id1, 'testdb.db')
#         self.assertIsNone(item1)

#         itm.deleteItem(self.id2, 'testdb.db')
#         item2 = itm.fetchItemFromId(self.id2, 'testdb.db')
#         self.assertIsNone(item2)

if __name__ == '__main__':
    unittest.main()