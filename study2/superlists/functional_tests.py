import unittest

from selenium                       import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By
from webdriver_manager.chrome       import ChromeDriverManager

from django.test import LiveServerTestCase



class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(3) # 암묵적 대기

    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,"h1").text
        print(header_text)
        self.assertIn('To-Do', header_text)
        
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1:공작깃털 사기')

        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # self.assertTrue(any(row.text == '1: 공작깃털 사기' for row in rows), 
        # "신규 작업이 테이블에 표시되지 않는다. -- 해당 텍스트:\n%s" %(table.text,
        # ))

        self.assertIn('1: 공작깃털 사기', [row.text for row in rows])

        self.fail('Finish the test!')

# if __name__  == '__main__':
#     unittest.main(warnings='ignore')
