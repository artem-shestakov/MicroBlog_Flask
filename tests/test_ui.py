import unittest
import time
from selenium import webdriver


class TestUI(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Firefox()

    def tearDown(self) -> None:
        self.driver.close()

    def test_add_new_post(self):
        """
        Tests if the new post page saves a Post object to the database
        """
        # Get Sign In page
        self.driver.get("http://127.0.0.1:5000/auth/login")

        # Find and filling fields
        email_field = self.driver.find_element_by_name("email")
        email_field.send_keys("test@test.com")
        time.sleep(1)

        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test")
        time.sleep(1)

        # Press the Sign In button
        sign_in_btn = self.driver.find_element_by_id("sign_in_btn")
        sign_in_btn.click()
        time.sleep(3)

        # Get new post form
        self.driver.get("http://127.0.0.1:5000/post/new")
        title_field = self.driver.find_element_by_name("title")
        title_field.send_keys("Test by Silenium")
        time.sleep(3)

        # Find CKEditor
        basic_page_body_xpath = "//div[contains(@id, 'cke_1_contents')]/iframe"
        ckeditor_frame = self.driver.find_element_by_xpath(basic_page_body_xpath)

        # Switch to iframe
        self.driver.switch_to.frame(ckeditor_frame)
        editor_body = self.driver.find_element_by_xpath("//body")
        editor_body.send_keys("Test content by Silenium")
        self.driver.switch_to.default_content()
        time.sleep(1)

        post_button = self.driver.find_element_by_class_name("btn-primary")
        post_button.click()

        # verify the post was created
        self.driver.get("http://localhost:5000/")
        time.sleep(2)
        self.assertIn("Test by Silenium", self.driver.page_source)
        self.assertIn("Test content by Silenium", self.driver.page_source)


if __name__ == '__main__':
    unittest.main()
