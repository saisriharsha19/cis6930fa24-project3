import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))
import unittest
import sqlite3
from project3 import func
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

        # Populate the database
        func.populatedb(self.db, incidents)

        # Directly query the database for counts
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature''')
        nature_counts = cur.fetchall()
        conn.close()

        # Convert the results to a dictionary for easier comparison
        count_dict = {nature: count for nature, count in nature_counts}

        # Define expected counts
        expected_counts = {
            'Vandalism': 2,
            'Larceny': 1
        }

        # Assert that the counts match the expected counts
        for nature, expected_count in expected_counts.items():
            self.assertEqual(count_dict.get(nature, 0), expected_count)

if __name__ == '__main__':
    unittest.main()
