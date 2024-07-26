import unittest
import database.items as itm

class healthCheck(unittest.TestCase):
    def test(self):
        self.assertEqual(itm.testFunction(), 'hello')