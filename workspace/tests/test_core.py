import pathlib
import unittest
from tempfile import TemporaryDirectory

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