import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class TestAppendItemToProjectId(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        prj.createProjectTable('testdb.db')

        self.item_id0 = itm.insertItem(owner=1, parent=0, position=0, content='hello', filename='testdb.db')
        self.item_id1 = itm.insertItem(owner=2, parent=0, position=0, content='bonjour', filename='testdb.db')
        self.item_id2 = itm.insertItem(owner=3, parent=0, position=0, content='ciao', filename='testdb.db')
        self.item_id3 = itm.insertItem(owner=3, parent=0, position=0, content='hola', filename='testdb.db')

        self.project_id0 = prj.insertProject(owner=1, title='Test Project', position = 0, filename='testdb.db')
        self.project_id1 = prj.insertProject(owner=2, title='Test Project 2', position = 1, filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testWasAdded(self):
        items = itm.fetchItemIdCollectionFromProjectId(self.project_id0, 'testdb.db')
        self.assertEqual(len(items), 0)

        prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=self.project_id0, filename='testdb.db')
        items = itm.fetchItemIdCollectionFromProjectId(self.project_id0, 'testdb.db')
        self.assertEqual(len(items), 1)

        prj.appendItemToProjectChildren(item_id=self.item_id1, project_id=self.project_id0, filename='testdb.db')
        items = itm.fetchItemIdCollectionFromProjectId(self.project_id0, 'testdb.db')
        self.assertEqual(len(items), 2)

        prj.appendItemToProjectChildren(item_id=self.item_id2, project_id=self.project_id0, filename='testdb.db')
        items = itm.fetchItemIdCollectionFromProjectId(self.project_id0, 'testdb.db')
        self.assertEqual(len(items), 3)

        prj.appendItemToProjectChildren(item_id=self.item_id3, project_id=self.project_id0, filename='testdb.db')
        items = itm.fetchItemIdCollectionFromProjectId(self.project_id0, 'testdb.db')
        self.assertEqual(len(items), 4)


    def testIsTrue(self):
        success0 = prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=self.project_id0, filename='testdb.db')
        success1 = prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=self.project_id0, filename='testdb.db')
        success2 = prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=self.project_id0, filename='testdb.db')
        success3 = prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=self.project_id0, filename='testdb.db')
        success = [success0, success1, success2, success3]
        for succ in success:
            self.assertTrue(succ)

    def testProjectNotExists(self):
        success0 = prj.appendItemToProjectChildren(item_id=self.item_id0, project_id=4342524, filename='testdb.db')
        success1 = prj.appendItemToProjectChildren(item_id=self.item_id1, project_id=4342524, filename='testdb.db')
        success2 = prj.appendItemToProjectChildren(item_id=self.item_id2, project_id=4342524, filename='testdb.db')
        success3 = prj.appendItemToProjectChildren(item_id=self.item_id3, project_id=4342524, filename='testdb.db')
        success = [success0, success1, success2, success3]
        for succ in success:
            self.assertFalse(succ)

class TestGetItemOrder(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        prj.createProjectTable('testdb.db')

        self.item_id0 = itm.insertItem(owner=1, parent=1, position=1, content='hello', filename='testdb.db')
        self.item_id1 = itm.insertItem(owner=1, parent=1, position=2, content='bonjour', filename='testdb.db')
        self.item_id2 = itm.insertItem(owner=1, parent=1, position=3, content='ciao', filename='testdb.db')
        self.item_id3 = itm.insertItem(owner=1, parent=1, position=4, content='hola', filename='testdb.db')
        self.order = [self.item_id0, self.item_id1, self.item_id2, self.item_id3]

        self.project_id0 = prj.insertProject(owner=1, title='Test Project', position = 0, filename='testdb.db')
        self.project_id1 = prj.insertProject(owner=1, title='Test Project', position = 0, filename='testdb.db')


    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')

    def testOutputIsCorrect(self):
        output = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
        self.assertEqual(self.order, output)

    def testOutputIsNotCorrect(self):
        output = itm.getItemOrder(project_id=10000, filename='testdb.db')
        self.assertEqual(output, [])
    
    def testFormattedOutputIsAList(self):
        output = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
        self.assertIsInstance(output, list)


##TODO: Finish this

class TestSetNewItemOrder(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        prj.createProjectTable('testdb.db')

        self.item_id0 = itm.insertItem(owner=1, parent=1, position=1, content='hello', filename='testdb.db')
        self.item_id1 = itm.insertItem(owner=1, parent=1, position=2, content='bonjour', filename='testdb.db')
        self.item_id2 = itm.insertItem(owner=1, parent=1, position=3, content='ciao', filename='testdb.db')
        self.item_id3 = itm.insertItem(owner=1, parent=1, position=4, content='hola', filename='testdb.db')
        self.order = [self.item_id0, self.item_id1, self.item_id2, self.item_id3]

        self.project_id0 = prj.insertProject(owner=1, title='Test Project', position = 0, filename='testdb.db')
        self.project_id1 = prj.insertProject(owner=1, title='Test Project', position = 0, filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testOrder0(self):
        #TODO: this is not an actual test
        order = [1, 2, 3, 4]
        itm.getItemOrder(project_id = self.project_id0, filename='testdb.db')
        itm.setNewItemOrder(self.project_id0, order=order, filename='testdb.db')

## DEPRECATED
# class TestRemoveItemIdFromProjectItems(unittest.TestCase):
#     def setUp(self):
#         itm.createItemTable('testdb.db')
#         prj.createProjectTable('testdb.db')

#         self.project_id0 = prj.insertProject(
#             owner=1,
#             title='Test Project',
#             position = 0, 
#             filename='testdb.db'
#             )
#         self.item0 = itm.insertItem(owner=1, parent = self.project_id0, position = 0, content='ciao', filename='testdb.db')
#         self.item1 = itm.insertItem(owner=1, parent = self.project_id0, position = 0, content='hello', filename='testdb.db')
#         self.item2 = itm.insertItem(owner=1, parent = self.project_id0, position = 0, content='bonjour', filename='testdb.db')
#         self.item3 = itm.insertItem(owner=1, parent = self.project_id0, position = 0, content='hola', filename='testdb.db')
        
#     def tearDown(self):
#         if os.path.exists('testdb.db') == True:
#             os.remove('testdb.db')
#         else:
#             raise FileNotFoundError('testdb.db does not seem to exist')
    
#     def testLength(self):
#         items = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
#         self.assertEqual(len(items), 4)

#         itm.removeItemIdFromProjectItems(
#             item_id=self.item0, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#             )
#         items = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
#         self.assertEqual(len(items), 3)

#         itm.removeItemIdFromProjectItems(
#             item_id=self.item1, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#             )
#         items = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
#         self.assertEqual(len(items), 2)

#         itm.removeItemIdFromProjectItems(
#             item_id=self.item2, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#             )
#         items = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
#         self.assertEqual(len(items), 1)

#         itm.removeItemIdFromProjectItems(
#             item_id=self.item3, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#             )
#         items = itm.getItemOrder(project_id=self.project_id0, filename='testdb.db')
#         self.assertEqual(len(items), 0)

#     def testRemoval(self):
#         result = itm.findProjectWithItemId(item_id=self.item0, filename='testdb.db')
#         self.assertIsInstance(result, int)
#         itm.removeItemIdFromProjectItems(
#             item_id=self.item0, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#         )
#         result = itm.findProjectWithItemId(item_id=self.item0, filename='testdb.db')
#         self.assertIsNone(result)

#         result = itm.findProjectWithItemId(item_id=self.item1, filename='testdb.db')
#         self.assertIsInstance(result, int)
#         itm.removeItemIdFromProjectItems(
#             item_id=self.item1, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#         )
#         result = itm.findProjectWithItemId(item_id=self.item1, filename='testdb.db')
#         self.assertIsNone(result)

#         result = itm.findProjectWithItemId(item_id=self.item2, filename='testdb.db')
#         self.assertIsInstance(result, int)
#         itm.removeItemIdFromProjectItems(
#             item_id=self.item2, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#         )
#         result = itm.findProjectWithItemId(item_id=self.item2, filename='testdb.db')
#         self.assertIsNone(result)

#         result = itm.findProjectWithItemId(item_id=self.item3, filename='testdb.db')
#         self.assertIsInstance(result, int)
#         itm.removeItemIdFromProjectItems(
#             item_id=self.item3, 
#             project_id = self.project_id0, 
#             filename='testdb.db'
#         )
#         result = itm.findProjectWithItemId(item_id=self.item3, filename='testdb.db')
#         self.assertIsNone(result)

    def testOutputIsTrue(self):
        pass

    def testIdNotExisting(self):
        pass
    def testIdNone(self):
        pass
    #TODO finish this
    
        
if __name__ == '__main__':
    unittest.main()