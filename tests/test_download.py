import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))
import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock
from project0 import func
class TestDownloadAndExtractIncidents(unittest.TestCase):
    
    @patch('project0.func.requests.get')
    def test_fetchincidents(self, mock_get):
        # Mocking a successful PDF fetch
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'%PDF-1.4 mock pdf content'  # Placeholder content
        mock_get.return_value = mock_response

        result = func.fetchincidents("http://example.com/fakeurl.pdf")

        self.assertIsInstance(result, BytesIO)

    @patch('project0.func.PdfReader')
    def test_extractincidents(self, mock_PdfReader):
        mock_reader = MagicMock()
        mock_reader.pages = [MagicMock(), MagicMock()]

        mock_reader.pages[0].extract_text.return_value = (
            "8/6/2024 19:24 2024-00056880 15905 LOLA RD Vandalism OK0140200\n"
        )
        mock_reader.pages[1].extract_text.return_value = (
            "8/7/2024 14:12 2024-00056881 15906 LOLA RD Larceny OK0140200\n"
        )
        mock_PdfReader.return_value = mock_reader

        incidents = func.extractincidents(mock_reader)

        expected = [
            ['8/6/2024 19:24', '2024-00056880', '15905 LOLA RD', 'Vandalism', 'OK0140200'],
            ['8/7/2024 14:12', '2024-00056881', '15906 LOLA RD', 'Larceny', 'OK0140200']
        ]
        self.assertEqual([incidents[0],incidents[2]], expected)

if __name__ == '__main__':
    unittest.main()

