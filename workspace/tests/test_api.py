import unittest, sys, json
from io import StringIO
from unittest.mock import patch, MagicMock

class BuildUrlTest(unittest.TestCase):
    def test_build_url(self):
        from booksearch.api import build_url
        expected = 'https://www.googleapis.com/books/v1/volumes?q=python'
        actual = build_url({'q':'python'})
        self.assertEqual(expected, actual)
    
    def test_build_url_empty_param(self):
        from booksearch.api import build_url
        expected = 'https://www.googleapis.com/books/v1/volumes?'
        actual = build_url({})
        self.assertEqual(expected, actual)
    
    @unittest.expectedFailure
    def test_build_url_fail(self):
        from booksearch.api import build_url
        expected = 'https://www.googleapis.com/books/v1/volumes'
        actual = build_url({})
        self.assertEqual(expected, actual, msg='이 테스트는 실패합니다')
    
    # 테스트 케이스를 남겨두었거나, 특정 테스트 케이스를 건너뛰고 싶을 때
    @unittest.skip('this is a skip test')
    def test_nothing_skip(self):
        pass

    @unittest.skipIf(sys.version_info > (3, 6), 'this is a skipIf test')
    def test_nothing_skipIf(self):
        pass

# subTest 메소드를 사용해 수행하는 테스트로, with 블록 하나가 테스트 케이스 하나에 해당
# subTest 메소드에 실패 시 도움이 되는 임의의 키워드 인수를 전달
# 파라미터를 바꾸어 가면서 여러 차례 실행한느 테스트 케이스

class BuildUrlMultiTest(unittest.TestCase):
    def test_build_url_multi(self):
        from booksearch.api import build_url
        base = 'https://www.googleapis.com/books/v1/volumes?'
        expected_url = f'{base}q=python'

        params = (
            (expected_url, {'q':'python'}),
            (expected_url, {'q':'python', 'maxResults':1}),
            (expected_url, {'q':'python', 'langRestrict':'en'})
        )

        for expected, param in params:
            with self.subTest(**param):
                actual = build_url(param)
                self.assertEqual(expected, actual)

class GetJsonTest(unittest.TestCase):
    def test_get_json(self):
        from booksearch.api import get_json
        with patch('booksearch.api.request.urlopen') as mock_urlopen:
            expected_response = {'id':'test'}
            fp = StringIO(json.dumps(expected_response))
            mock = MagicMock()
            mock.__enter__.return_value = fp
            mock_urlopen.return_value = mock
            actual = get_json({'p':'python'})
            self.assertEqual(expected_response, actual)


