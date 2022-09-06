from importlib.resources import path
import pathlib
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import URLError

THUMBNAIL_URL = (
    'https://books.google.com/books/content'
    '?id=OgtBw760Y5EC&printsec=frontcover'
    '&img=1&zoom=1&edge=curl&source=gbs_api'
)

class SaveThumbnailsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_thumbnails(self):
        from booksearch.core import Book
        book = Book({'id':'', 'volumeInfo':{
            'imageLinks':{
                'thumbnail':THUMBNAIL_URL
            }
        }})

        filename = book.save_thumbnails(self.tmp.name)[0]
        self.assertTrue(pathlib.Path(filename).exists())

class SaveThumbnailsTest2(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    @patch('booksearch.core.get_data')
    def test_save_thumbnails2(self, mock_get_data):
        from booksearch.core import Book
        data_path = pathlib.Path(__file__).with_name('data')
        mock_get_data.return_value = (data_path / 'xD96CAAAQBAJ_thumbnail.jpeg').read_bytes()

        book = Book({'id':'', 'volumeInfo': {
            'thumbnail': THUMBNAIL_URL
            }})
        filename = book.save_thumbnails(self.tmp.name)[1]

        mock_get_data.assert_called_with(THUMBNAIL_URL)

        self.assertEqual(data, filename.read_bytes())

class GetBooksTest(unittest.TestCase):
    def test_get_books_no_connection(self):
        from booksearch.core import get_books

        with patch('socket.socket.connect') as mock:
            mock.return_value = None

            with self.assertRaisesRegex(URLError, 'urlopen error'):
                get_books(q='python')

