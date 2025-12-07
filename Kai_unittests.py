
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

YOUFACE_LOGIN_URL = "http://127.0.0.1:8000/login" 
VALID_USERNAME = "Jeff"
VALID_PASSWORD = "Gumby"
INVALID_USERNAME = "baduser"
INVALID_PASSWORD = "badpassword"
TIMEOUT = 5

class YoufaceLoginPageTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print(f"\nBeginning Tests - John Doe")
        cls.driver = webdriver.Chrome() 
        cls.driver.implicitly_wait(TIMEOUT)
    
    def setUp(self):
        self.driver.get(YOUFACE_LOGIN_URL)
        self.assertIn("Login", self.driver.title)
        self.ran_tests = 0
        self.passed_tests = 0
    
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        print("\nEnding Tests:")
        cls.driver.quit()

    def _report_result(self, test_name, success, message=""):
        result = "[PASSED]" if success else "[FAILED]"
        output = f"{result} - {test_name}"
        if not success:
            output += f" ({message})"
        print(output)
        self.ran_tests += 1
        if success:
            self.passed_tests += 1
        return success
    
    def test_01_login_button_exists(self):
        try:
            login_button = self.driver.find_element(By.ID, "login-submit-button")
            success = login_button is not None
            self._report_result("Login Button Exists", success)
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Login Button Exists", False, "Element not found by ID 'login-submit-button'")
            self.fail("Login Button not found.")

    def test_02_login_button_is_green(self):
        try:
            login_button = self.driver.find_element(By.ID, "login-submit-button")
            color = login_button.value_of_css_property("background-color")
            expected_color = "rgba(0, 128, 0, 1)" 
            success = color == expected_color
            self._report_result("Login Button is Green", success, f"Found color: {color}")
            self.assertTrue(success)
        except Exception as e:
            self._report_result("Login Button is Green", False, f"Error checking color: {e}")
            self.fail(f"Test failed: {e}")
    
    def test_03_create_user_link_exists(self):
        try:
            create_link = self.driver.find_element(By.LINK_TEXT, "Create New Account")
            success = create_link is not None
            self._report_result("Create User Link Exists", success)
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Create User Link Exists", False, "Link not found with text 'Create New Account'")
            self.fail("Create User Link not found.")

    def test_04_username_field_is_present(self):
        try:
            username_field = self.driver.find_element(By.ID, "id_username")
            success = username_field is not None
            self._report_result("Username Field is Present", success)
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Username Field is Present", False, "Input field not found by ID 'id_username'")
            self.fail("Username field not found.")

    def test_05_password_field_is_present(self):
        try:
            password_field = self.driver.find_element(By.ID, "id_password")
            is_password_type = password_field.get_attribute("type") == "password"
            success = password_field is not None and is_password_type
            self._report_result("Password Field is Present and Masked", success, f"Type: {password_field.get_attribute('type')}")
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Password Field is Present and Masked", False, "Input field not found by ID 'id_password'")
            self.fail("Password field not found.")

    def test_06_login_succeeds_valid_credentials(self):
        self.driver.find_element(By.ID, "id_username").send_keys(VALID_USERNAME)
        self.driver.find_element(By.ID, "id_password").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.ID, "login-submit-button").click()
        
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.url_changes(YOUFACE_LOGIN_URL)
            )
            welcome_text = self.driver.find_element(By.TAG_NAME, "h1").text
            success = "Welcome" in welcome_text or "Dashboard" in self.driver.title
            self._report_result(f"Login Succeeds with Username '{VALID_USERNAME}' and Password '...' ", success, "Did not land on dashboard or welcome page")
            self.assertTrue(success)
        except TimeoutException:
            self._report_result(f"Login Succeeds with Username '{VALID_USERNAME}' and Password '...' ", False, "Timeout: Did not redirect after login.")
            self.fail("Login failed or timed out.")

    def test_07_login_fails_invalid_username(self):
        self.driver.find_element(By.ID, "id_username").send_keys(INVALID_USERNAME)
        self.driver.find_element(By.ID, "id_password").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.ID, "login-submit-button").click()
        
        error_message_xpath = "//div[@id='login-error' or contains(@class, 'error-message')]" 
        try:
            error_element = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, error_message_xpath))
            )
            is_on_login_page = YOUFACE_LOGIN_URL in self.driver.current_url
            success = is_on_login_page and error_element.is_displayed()
            self._report_result("Login Fails with invalid Username", success, f"Error message visible: {error_element.text}")
            self.assertTrue(success)
        except TimeoutException:
            self._report_result("Login Fails with invalid Username", False, "Timeout: Error message did not appear or was redirected.")
            self.fail("Login unexpectedly succeeded or failed to display error.")

    def test_08_login_fails_invalid_password(self):
        self.driver.find_element(By.ID, "id_username").send_keys(VALID_USERNAME)
        self.driver.find
