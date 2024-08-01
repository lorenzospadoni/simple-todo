import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testTestFunction(unittest.TestCase):
    def test(self):
        self.assertEqual(itm.testFunction(), 'hello')


if __name__ == '__main__':
    unittest.main()