import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class TestGetProjectPosition(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable(filename='testdb.db')
        self.project0 = prj.insertProject(owner = 2, title='ciao', position = 1, filename='testdb.db')
        self.project1 = prj.insertProject(owner = 2, title='hello', position = 2, filename='testdb.db')
        self.project2 = prj.insertProject(owner = 2, title='bonjour', position = 3, filename='testdb.db')
        self.project3 = prj.insertProject(owner = 2, title='hola', position = 4, filename='testdb.db')
               
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testProjectPositionIsCorrect(self):
        position = prj.getProjectPosition(project_id=self.project0, filename='testdb.db')
        self.assertEqual(position, 1)

        position = prj.getProjectPosition(project_id=self.project1, filename='testdb.db')
        self.assertEqual(position, 2)

        position = prj.getProjectPosition(project_id=self.project2, filename='testdb.db')
        self.assertEqual(position, 3)

        position = prj.getProjectPosition(project_id=self.project3, filename='testdb.db')
        self.assertEqual(position, 4)

    def testProjectPositionIsNotCorrect(self):
        position = prj.getProjectPosition(project_id=6456, filename='testdb.db')
        self.assertIsNone(position)

        position = prj.getProjectPosition(project_id=4234, filename='testdb.db')
        self.assertIsNone(position)

        position = prj.getProjectPosition(project_id=34, filename='testdb.db')
        self.assertIsNone(position)

        position = prj.getProjectPosition(project_id=6, filename='testdb.db')
        self.assertIsNone(position)

class TestGetBiggestPosition(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable(filename='testdb.db')
        self.project0 = prj.insertProject(owner = 2, title='ciao', position = 1, filename='testdb.db')
        self.project1 = prj.insertProject(owner = 2, title='hello', position = 2, filename='testdb.db')
        self.project2 = prj.insertProject(owner = 2, title='bonjour', position = 3, filename='testdb.db')
        self.project3 = prj.insertProject(owner = 2, title='hola', position = 4, filename='testdb.db')
               
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testBiggestPositionExists(self):
        result = prj.getBiggestPosition(user_id=2, filename='testdb.db')
        self.assertEqual(result, 4)

    def testBiggestPositionDoesNotExist(self):
        result0 = prj.getBiggestPosition(user_id = 60, filename='testdb.db')
        result1 = prj.getBiggestPosition(user_id = 354, filename='testdb.db')
        result2 = prj.getBiggestPosition(user_id = 23, filename='testdb.db')
        result3 = prj.getBiggestPosition(user_id = 656, filename='testdb.db')

        results = [result0, result1, result2, result3]

        for result in results:
            self.assertEqual(result, 0)

class TestUpdateProjectPosition(unittest.TestCase):
    def setUp(self):
        prj.createProjectTable(filename='testdb.db')
        self.project_id = prj.insertProject(owner = 2, title='ciao', position = 1, filename='testdb.db')
 
    def tearDown(self):
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
    
    def testPositionUpdatedReturnTrue(self):
        result = prj.updateProjectPosition(project_id=self.project_id, position=5, filename='testdb.db')
        self.assertTrue(result)

        result = prj.updateProjectPosition(project_id=self.project_id, position=8, filename='testdb.db')
        self.assertTrue(result)

        result = prj.updateProjectPosition(project_id=self.project_id, position=3, filename='testdb.db')
        self.assertTrue(result)

        result = prj.updateProjectPosition(project_id=self.project_id, position=46, filename='testdb.db')
        self.assertTrue(result)

    def testPositionUpdatedReturnFalse(self):
        result = prj.updateProjectPosition(project_id=1000, position=5, filename='testdb.db')
        self.assertFalse(result)

        result = prj.updateProjectPosition(project_id=453, position=8, filename='testdb.db')
        self.assertFalse(result)

        result = prj.updateProjectPosition(project_id=67, position=3, filename='testdb.db')
        self.assertFalse(result)

        result = prj.updateProjectPosition(project_id=7554, position=46, filename='testdb.db')
        self.assertFalse(result)


    def testPositionIsChanged(self):
        prj.updateProjectPosition(project_id = self.project_id, position=20, filename='testdb.db')
        position = prj.getProjectPosition(project_id = self.project_id, filename='testdb.db')
        self.assertEqual(position, 20)

        prj.updateProjectPosition(project_id = self.project_id, position=55, filename='testdb.db')
        position = prj.getProjectPosition(project_id = self.project_id, filename='testdb.db')
        self.assertEqual(position, 55)

if __name__ == '__main__':
    unittest.main()