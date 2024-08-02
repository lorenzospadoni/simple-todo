import unittest, sqlite3, os, json
import database.items as itm
import database.projects as prj

class testFromRecordToItem(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        record0 = (30, 5, 'Ciao', '2024-10-15 20:22:1721943498')
        record1 = (30, 34, 'Hello', '2024-07-25 23:38:1721943498')
        record2 = (30, 99, 'Bonjour', '2024-10-6 23:38:1721943498')
        record3 = (None, )
        record4 = (None)
        self.item0 = itm.fromRecordToItem(record0)
        self.item1 = itm.fromRecordToItem(record1)
        self.item2 = itm.fromRecordToItem(record2)
        self.item3 = itm.fromRecordToItem(record3)
        self.item4 = itm.fromRecordToItem(record4)

    def tearDown(self):
        # os.remove('testdb.db')
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testOutputIsInstanceOfItem(self):
        self.assertEqual(type(self.item0), itm.Item)
        self.assertEqual(type(self.item1), itm.Item)
        self.assertEqual(type(self.item2), itm.Item)
    
    def testEmptyRecordsAreNone(self):
        self.assertIsNone(self.item3)
        self.assertIsNone(self.item4)

class testFromRecordToItemCollection(unittest.TestCase):
    def setUp(self):
        itm.createItemTable('testdb.db')
        self.test_records0 = (
            (30, 5, 'Ciao', '2024-10-15 20:22:1721943498'),
            (30, 34, 'Hello', '2024-07-25 23:38:1721943498'),
            (30, 99, 'Bonjour', '2024-10-6 23:38:1721943498')
        )
        self.test_records1 = (None, )
        self.test_records2 = None
        self.test_records3 = (
            (30, 5, 'Ciao', '2024-10-15 20:22:1721943498'),
            None,
        )

    def tearDown(self):
        # os.remove('testdb.db')
        if os.path.exists('testdb.db') == True:
            os.remove('testdb.db')
        else:
            raise FileNotFoundError('testdb.db does not seem to exist')
        
    def testOutputIsList(self):
        items = itm.fromRecordsToItemCollection(self.test_records0)
        items1 = itm.fromRecordsToItemCollection(self.test_records1)
        items2 = itm.fromRecordsToItemCollection(self.test_records2)
        items3 = itm.fromRecordsToItemCollection(self.test_records3)
        self.assertEqual(type(items), list)
        self.assertEqual(type(items1), list)
        self.assertEqual(type(items2), list)
        self.assertEqual(type(items3), list)

         
    def testOutputItemsAreInstanceOfItem(self):
        items = itm.fromRecordsToItemCollection(self.test_records0)

        for item in items:
            self.assertEqual(type(item), itm.Item)
    
    def testEmptyRecordsAreList(self):
        items1 = itm.fromRecordsToItemCollection(self.test_records1)
        items2 = itm.fromRecordsToItemCollection(self.test_records2)

        self.assertEqual(items1, [])
        self.assertEqual(items2, [])

    def testNoneTypesAreRemoved(self):
        items = itm.fromRecordsToItemCollection(self.test_records3)
        self.assertEqual(len(items), 1)

if __name__ == '__main__':
    unittest.main()


