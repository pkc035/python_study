from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3) # 암묵적 대기

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://127.0.0.1:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__  == '__main__':
    unittest.main(warnings='ignore')
