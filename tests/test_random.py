import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import sqlite3
import func 
import os

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Prepare test database
        self.db = 'test_incidents.db'
        func.createdb(self.db)

    def tearDown(self):
        # Cleanup test database file
        if os.path.exists(self.db):
            os.remove(self.db)

    def test_createdb(self):
        # Test if the database and table are created successfully
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
        table_exists = cur.fetchone()
        conn.close()

        self.assertIsNotNone(table_exists)

    def test_populatedb(self):
        # Test data insertion
        incidents = [
            ['8/6/2024 19:24', '2024-00056880', '15905 LOLA RD', 'Vandalism', 'OK0140200'],
            ['8/7/2024 14:12', '2024-00056881', '15906 LOLA RD', 'Larceny', 'OK0140200']
        ]
        
        func.populatedb(self.db, incidents)

        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM incidents;")
        rows = cur.fetchall()
        conn.close()

        self.assertEqual(len(rows), 2)

    def test_status(self):
        # Test statistics generation
        incidents = [
            ['8/6/2024 19:24', '2024-00056880', '15905 LOLA RD', 'Vandalism', 'OK0140200'],
            ['8/7/2024 14:12', '2024-00056881', '15906 LOLA RD', 'Larceny', 'OK0140200'],
            ['8/8/2024 10:00', '2024-00056882', '15907 LOLA RD', 'Vandalism', 'OK0140200']
        ]
        
        func.populatedb(self.db, incidents)
        
        # Capture printed output
        with self.assertLogs(level='INFO') as log:
            func.status(self.db)
            output = log.output

        # Verify correct count of nature occurrences
        self.assertIn("Vandalism: 2 times", output[0])
        self.assertIn("Larceny: 1 time", output[0])

if __name__ == '__main__':
    unittest.main()
