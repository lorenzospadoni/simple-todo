import unittest
import sqlite3
import os

import database.utils as utl

# Assume the functions are imported from the module where they are defined.
# from your_module import execQuery, execLastRowId, execRowcount, execFetchone, execFetchall

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        """ Set up a temporary database for testing. """
        self.db_file = 'testdb.db'
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        
        # Create a sample table for testing
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                age INTEGER)''')
        self.connection.commit()

    def tearDown(self):
        """ Tear down the test database. """
        self.connection.close()
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        else:
            raise FileNotFoundError(f'{self.db_file} does not seem to exist')

    def test_execQuery(self):
        query = "INSERT INTO users (name, age) VALUES (?, ?)"
        args = ("Alice", 30)
        utl.execQuery(query, args, filename=self.db_file)

        # Verify that the row was inserted
        self.cursor.execute("SELECT * FROM users WHERE name = ?", ("Alice",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Alice")
        self.assertEqual(result[2], 30)

    def test_execLastRowId(self):
        query = "INSERT INTO users (name, age) VALUES (?, ?)"
        args = ("Bob", 25)
        last_row_id = utl.execLastRowId(query, args, filename=self.db_file)

        # Verify that the returned last_rowid is correct
        self.assertIsNotNone(last_row_id)
        self.cursor.execute("SELECT id FROM users WHERE id = ?", (last_row_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], last_row_id)

    def test_execRowcount(self):
        query = "INSERT INTO users (name, age) VALUES (?, ?)"
        args = ("Charlie", 40)
        rowcount = utl.execRowcount(query, args, filename=self.db_file)

        # Verify that the rowcount is correct (1 row inserted)
        self.assertEqual(rowcount, 1)

        # Update a record and check the rowcount
        update_query = "UPDATE users SET age = ? WHERE name = ?"
        update_args = (41, "Charlie")
        update_rowcount = utl.execRowcount(update_query, update_args, filename=self.db_file)
        self.assertEqual(update_rowcount, 1)

        # Delete a record and check the rowcount
        delete_query = "DELETE FROM users WHERE name = ?"
        delete_args = ("Charlie",)
        delete_rowcount = utl.execRowcount(delete_query, delete_args, filename=self.db_file)
        self.assertEqual(delete_rowcount, 1)

    def test_execFetchone(self):
        query = "INSERT INTO users (name, age) VALUES (?, ?)"
        args = ("David", 35)
        utl.execQuery(query, args, filename=self.db_file)

        fetch_query = "SELECT * FROM users WHERE name = ?"
        fetch_args = ("David",)
        result = utl.execFetchone(fetch_query, fetch_args, filename=self.db_file)

        # Verify that the fetched record is correct
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "David")
        self.assertEqual(result[2], 35)

        # Verify that None is returned when no match is found
        fetch_args = ("Nonexistent",)
        result = utl.execFetchone(fetch_query, fetch_args, filename=self.db_file)
        self.assertIsNone(result)

    def test_execFetchall(self):
        # Insert multiple records
        utl.execQuery("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 28), filename=self.db_file)
        utl.execQuery("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 30), filename=self.db_file)

        fetch_query = "SELECT * FROM users WHERE name = ?"
        fetch_args = ("Eve",)
        results = utl.execFetchall(fetch_query, fetch_args, filename=self.db_file)

        # Verify that all matching records are fetched
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)

        # Verify that an empty list is returned when no matches are found
        fetch_args = ("Nonexistent",)
        results = utl.execFetchall(fetch_query, fetch_args, filename=self.db_file)
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()