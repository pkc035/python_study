# 220905

# 단위 테스트
# python -m unittest 를 입력하여 이 모듈의 테스트를 실행할 수 있음.

import unittest

def booksearch():
    return {}

class BookSearchTest(unittest.TestCase):
    def test_booksearch(self):
        self.assertEqual({}, booksearch())



