import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock
from project0 import func
class TestDownloadAndExtractIncidents(unittest.TestCase):
    
    @patch('func.requests.get')
    def test_fetchincidents(self, mock_get):
        # Mocking a successful PDF fetch
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'%PDF-1.4 mock pdf content'
        mock_get.return_value = mock_response

        # Fetch the incidents
        result = func.fetchincidents("http://example.com/fakeurl.pdf")

        # Ensure it's a BytesIO object
        self.assertIsInstance(result, BytesIO)

    @patch('func.PdfReader')
    def test_extractincidents(self, mock_PdfReader):
        # Mocking the PDF reader
        mock_reader = MagicMock()
        mock_reader.pages = [MagicMock(), MagicMock()]
        mock_reader.pages[0].extract_text.return_value = "8/6/2024 19:24 2024-00056880 15905 LOLA RD\nVandalism OK0140200\n"
        mock_reader.pages[1].extract_text.return_value = "8/7/2024 14:12 2024-00056881 15906 LOLA RD\nLarceny OK0140200\n"
        mock_PdfReader.return_value = mock_reader

        pdf_file = BytesIO(b'%PDF-1.4 mock pdf content')

        # Extract incidents
        incidents = func.extractincidents(pdf_file)
        
        # Check if data is extracted correctly
        expected = [
            ['8/6/2024 19:24', '2024-00056880', '15905 LOLA RD', 'Vandalism', 'OK0140200'],
            ['8/7/2024 14:12', '2024-00056881', '15906 LOLA RD', 'Larceny', 'OK0140200']
        ]

        self.assertEqual(incidents, expected)

if __name__ == '__main__':
    unittest.main()
