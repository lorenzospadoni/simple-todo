import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testInsertProject(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable('testdb.db')
        self.a_id = prj.insertProject(owner=1, title='hello', position=1, filename='testdb.db')
        self.b_id = prj.insertProject(owner=2, title='bonjour', position=2, filename='testdb.db')
        self.c_id = prj.insertProject(owner=3, title='ciao', position=3, filename='testdb.db')
        self.projects = prj.fetchProjects('testdb.db')
        self.a_project = self.projects[0]
        self.b_project = self.projects[1]
        self.c_project = self.projects[2]

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testItemsLength(self):
        self.assertEqual(len(self.projects), 3)

    def testItemIdMatches(self):
        self.assertEqual(self.a_id, self.a_project.id)
        self.assertEqual(self.b_id, self.b_project.id)
        self.assertEqual(self.c_id, self.c_project.id)
    
    def testOutputIsList(self):
        self.assertEqual(type(self.projects), list)

    def testOutputMembersAreItems(self):
        self.assertIsInstance(self.a_project, prj.Project)
        self.assertIsInstance(self.b_project, prj.Project)
        self.assertIsInstance(self.c_project, prj.Project)

class testProjectExists(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable('testdb.db')
        self.a_id = prj.insertProject(owner=1, title='hello', position=1, filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testTrue(self):
        result = prj.projectExists(self.a_id, filename='testdb.db')
        self.assertTrue(result)

    def testFalse(self):
        result = prj.projectExists(1000, filename='testdb.db')
        self.assertFalse(result)

    def testInvalid(self):
        pass

    #TODO: should this handle invalid requests as False?


class TestUpdateProjectTitle(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable('testdb.db')

        self.id0 = prj.insertProject(
            owner=1, 
            title='hello', 
            position = 1, 
            filename='testdb.db'
        )
        self.id1 = prj.insertProject(
            owner=2, 
            title='bonjour', 
            position = 2, 
            filename='testdb.db'
            )
        self.id2 = prj.insertProject(
            owner=3, 
            title='ciao', 
            position = 3, 
            filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testIfItemExistsTrue(self):
        result0 = prj.updateProjectTitle(self.id0, 'olleh', filename='testdb.db')
        result1 = prj.updateProjectTitle(self.id1, 'ruojnob', filename='testdb.db')
        result2 = prj.updateProjectTitle(self.id2, 'oaic', filename='testdb.db')
        self.assertTrue(result0)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def testIfItemNotExistsFalse(self):
        result0 = prj.updateProjectTitle(34, 'olleh', filename='testdb.db')
        result1 = prj.updateProjectTitle(22, 'ruojnob', filename='testdb.db')
        result2 = prj.updateProjectTitle(7, 'oaic', filename='testdb.db')
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertFalse(result2)

    def testIfContentIsChanged(self):
        result0 = prj.updateProjectTitle(self.id0, 'olleh', filename='testdb.db')
        result1 = prj.updateProjectTitle(self.id1, 'ruojnob', filename='testdb.db')
        result2 = prj.updateProjectTitle(self.id2, 'oaic', filename='testdb.db')
        projects = prj.fetchProjectCollectionFromProjectIds([self.id0, self.id1, self.id2], filename='testdb.db')
        self.assertEqual(projects[0].title, 'olleh')
        self.assertEqual(projects[1].title, 'ruojnob')
        self.assertEqual(projects[2].title, 'oaic')

class TestDeleteProject(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable('testdb.db')

        self.id0 = prj.insertProject(
            owner=1, 
            title='hello', 
            position = 1, 
            filename='testdb.db')
        self.id1 = prj.insertProject(
            owner=2, 
            title='bonjour', 
            position = 2, 
            filename='testdb.db'
            )
        self.id2 = prj.insertProject(
            owner=3, 
            title='ciao', 
            position = 3, 
            filename='testdb.db')

    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testItemLength(self):
        prj.deleteProject(self.id0, 'testdb.db')
        projects = prj.fetchProjects('testdb.db')
        self.assertEqual(len(projects), 2)

        prj.deleteProject(self.id1, 'testdb.db')
        projects = prj.fetchProjects('testdb.db')
        self.assertEqual(len(projects), 1)

        prj.deleteProject(self.id2, 'testdb.db')
        projects = prj.fetchProjects('testdb.db')
        self.assertEqual(len(projects), 0)

    def testIfProjectExistsTrue(self):
        result0 = prj.deleteProject(self.id0, 'testdb.db')
        result1 = prj.deleteProject(self.id1, 'testdb.db')
        result2 = prj.deleteProject(self.id2, 'testdb.db')
        self.assertTrue(result0)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def testIfProjectNotExistsFalse(self):
        result0 = prj.deleteProject(1000, 'testdb.db')
        result1 = prj.deleteProject(100, 'testdb.db')
        result2 = prj.deleteProject(44, 'testdb.db')
        self.assertFalse(result0)
        self.assertFalse(result1)
        self.assertFalse(result2)
    
    def testDeletionRemovesId(self):
        prj.deleteProject(self.id0, 'testdb.db')
        project0 = prj.fetchProjectFromProjectId(self.id0, 'testdb.db')
        self.assertIsNone(project0)

        prj.deleteProject(self.id1, 'testdb.db')
        project1 = prj.fetchProjectFromProjectId(self.id1, 'testdb.db')
        self.assertIsNone(project1)

        prj.deleteProject(self.id2, 'testdb.db')
        project2 = prj.fetchProjectFromProjectId(self.id2, 'testdb.db')
        self.assertIsNone(project2)
### DEPRECATED
class TestDeleteProjectItems(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        prj.createProjectTable('testdb.db')

        self.id0 = prj.insertProject(
            owner=1, 
            title='hello', 
            position = 1, 
            filename='testdb.db')
        self.id1 = prj.insertProject(
            owner=2, 
            title='bonjour', 
            position = 2, 
            filename='testdb.db'
            )
        self.id2 = prj.insertProject(
            owner=3, 
            title='ciao', 
            position = 3, 
            filename='testdb.db')

        self.item0 = itm.insertItem(owner = 1, parent=self.id0, position=1, content = 'test0', filename='testdb.db')
        self.item1 = itm.insertItem(owner = 1, parent=self.id0, position=2, content = 'test1', filename='testdb.db')
        self.item2 = itm.insertItem(owner = 1, parent=self.id0, position=3, content = 'test2', filename='testdb.db')

        self.item3 = itm.insertItem(owner = 1, parent=self.id1, position=1, content = 'test3', filename='testdb.db')
        self.item4 = itm.insertItem(owner = 1, parent=self.id1, position=2, content = 'test4', filename='testdb.db')
        self.item5 = itm.insertItem(owner = 1, parent=self.id1, position=3, content = 'test5', filename='testdb.db')

        self.item6 = itm.insertItem(owner = 1, parent=self.id2, position=1, content = 'test6', filename='testdb.db')
        self.item7 = itm.insertItem(owner = 1, parent=self.id2, position=2, content = 'test7', filename='testdb.db')
        self.item8 = itm.insertItem(owner = 1, parent=self.id2, position=3, content = 'test8', filename='testdb.db')

        self.items = [
            self.item0, 
            self.item1,
            self.item2,
            self.item3,
            self.item4,
            self.item5,
            self.item6, 
            self.item7, 
            self.item8, 
        ]


        
        
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testDeletingItems(self):
        prj.deleteProjectItems(project_id = self.id0, filename='testdb.db')
        prj.deleteProjectItems(project_id = self.id1, filename='testdb.db')
        prj.deleteProjectItems(project_id = self.id2, filename='testdb.db')
        for item_id in self.items:
            result = itm.fetchItemFromId(item_id = item_id, filename = 'testdb.db')
            self.assertIsNone(result)
    #TODO: should deleteProjectItems remove them from the items field of a project record?
    

##TODO: finish developing TestDeleteProjects
# class TestDeleteProjects(unittest.TestCase):
#     def setUp(self):
#         prj.createProjectTable('testdb.db')
#         self.id0 = prj.insertProject(owner=1, title='hello', items=[], position = 1, filename='testdb.db')
#         self.id1 = prj.insertProject(owner=2, title='bonjour', items=[], position = 2, filename='testdb.db')
#         self.id2 = prj.insertProject(owner=3, title='ciao', items=[], position = 3, filename='testdb.db')

#     def tearDown(self):
#         if os.path.exists('testdb.db') == True:
#             os.remove('testdb.db')self.item0,
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