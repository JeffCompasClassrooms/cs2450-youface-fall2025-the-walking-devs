import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time 

# --- CONFIGURATION ---
YOUFACE_LOGIN_URL = "http://127.0.0.1:5005/" 
VALID_USERNAME = "Kpond2" 
VALID_PASSWORD = "...."
INVALID_USERNAME = "invaliduser"
INVALID_PASSWORD = "invalidpassword"
TIMEOUT = 10 
YOUR_NAME = "Kai Pond" 
# ---------------------

class YoufaceLoginPageTests(unittest.TestCase):
    
    # Class variables to track results for the final summary
    ran_tests = 0
    passed_tests = 0

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome() 
        cls.driver.implicitly_wait(TIMEOUT) 
        # Print the starting banner
        print(f"Beginning Tests - {YOUR_NAME}") 
    
    def setUp(self):
        self.driver.get(YOUFACE_LOGIN_URL)
        self.assertIn("CampusTalk", self.driver.title)
    
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # Calculate and print the final summary (this uses the class variables updated in _report_result)
        print("\nEnding Tests:")
        print(f"{cls.ran_tests} Tests Ran: {cls.passed_tests} Tests Passed")
        cls.driver.quit()

    def _report_result(self, test_name, success, message=""):
        result = "[PASSED]" if success else "[FAILED]"
        output = f"{result} - {test_name}"
        if not success:
            output += f" ({message})"
        
        # 1. Print the result immediately to stdout
        print(output)
        
        # 2. Update the class counters for the final summary
        YoufaceLoginPageTests.ran_tests += 1
        if success:
            YoufaceLoginPageTests.passed_tests += 1
            
        return success
    
    # --- LOCATORS ---
    LOGIN_BUTTON_LOCATOR = (By.XPATH, "//*[self::input or self::button][(contains(translate(text(), 'LOGIN', 'login'), 'login') or contains(translate(@value, 'LOGIN', 'login'), 'login')) and not(contains(translate(text(), 'CREATE', 'create'), 'create')) and not(contains(translate(@value, 'CREATE', 'create'), 'create'))]")
    USERNAME_FIELD_LOCATOR = (By.NAME, "username") 
    PASSWORD_FIELD_LOCATOR = (By.NAME, "password")
    CREATE_LINK_LOCATOR = (By.XPATH, "//a[contains(@href, '/create')]") 
    ERROR_MESSAGE_LOCATOR = (By.XPATH, "//*[contains(translate(text(), 'ERROR', 'error'), 'error') or contains(translate(text(), 'FAIL', 'fail'), 'fail') or contains(translate(text(), 'INVALID', 'invalid'), 'invalid')]")
    # --------------------------

    # --- TEST 01: Login Button Exists ---
    def test_01_login_button_exists(self):
        try:
            login_button = self.driver.find_element(*self.LOGIN_BUTTON_LOCATOR)
            success = login_button is not None
            self._report_result("Login Button Exists", success)
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Login Button Exists", False, f"Could not find Login button.")
            self.fail("Login Button not found.")

    # --- TEST 02: Login Button Color ---
    def test_02_login_button_is_red(self):
        try:
            login_button = self.driver.find_element(*self.LOGIN_BUTTON_LOCATOR)
            color = login_button.value_of_css_property("background-color")
            expected_color = "rgba(208, 0, 0, 1)"  
            success = color == expected_color
            self._report_result("Login Button is Red", success, f"Found color: {color}") 
            self.assertTrue(success)
        except Exception as e:
            self._report_result("Login Button is Red", False, f"Error checking color: {e}")
            self.fail(f"Test failed: {e}")
    
    # --- TEST 03: Create User Link Exists ---
    def test_03_create_user_link_exists(self):
        try:
            create_link = self.driver.find_element(*self.CREATE_LINK_LOCATOR)
            success = create_link is not None
            self._report_result("Create User Link Exists", success) 
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Create User Link Exists", False, f"Could not find 'Create' link.")
            self.fail("Create User Link not found.")
            
    # --- TEST 04: Username Field is Present ---
    def test_04_username_field_is_present(self):
        try:
            username_field = self.driver.find_element(*self.USERNAME_FIELD_LOCATOR)
            success = username_field is not None
            self._report_result("Username Field is Present", success)
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Username Field is Present", False, f"Input field not found by {self.USERNAME_FIELD_LOCATOR}")
            self.fail("Username field not found.")

    # --- TEST 05: Password Field is Present ---
    def test_05_password_field_is_present(self):
        try:
            password_field = self.driver.find_element(*self.PASSWORD_FIELD_LOCATOR)
            is_password_type = password_field.get_attribute("type") == "password"
            success = password_field is not None and is_password_type
            self._report_result("Password Field is Present and Masked", success, f"Type: {password_field.get_attribute('type')}")
            self.assertTrue(success)
        except NoSuchElementException:
            self._report_result("Password Field is Present and Masked", False, f"Input field not found by {self.PASSWORD_FIELD_LOCATOR}")
            self.fail("Password field not found.")

    # --- TEST 06: Login Succeeds ---
    def test_06_login_succeeds_valid_credentials(self):
        
        WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located(self.USERNAME_FIELD_LOCATOR)).send_keys(VALID_USERNAME)
        self.driver.find_element(*self.PASSWORD_FIELD_LOCATOR).send_keys(VALID_PASSWORD)
        self.driver.find_element(*self.LOGIN_BUTTON_LOCATOR).click()
        
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.url_changes(YOUFACE_LOGIN_URL)
            )
            current_url = self.driver.current_url.lower().rstrip('/')
            success = current_url != YOUFACE_LOGIN_URL.lower().rstrip('/')
            self._report_result(f"Login Succeeds with Username '{VALID_USERNAME}' and Password '{VALID_PASSWORD}'", success, f"Current URL: {self.driver.current_url}")
            self.assertTrue(success)
        except TimeoutException:
            self._report_result(f"Login Succeeds with Username '{VALID_USERNAME}' and Password '{VALID_PASSWORD}'", False, "Timeout: Did not redirect after login.")
            self.fail("Login failed or timed out.")

    # --- TEST 07: Create User Link Navigates Correctly ---
    def test_07_create_user_link_navigation(self):
        create_link = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(self.CREATE_LINK_LOCATOR)
        )
        create_link.click()
        
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.url_contains("/create")
            )
            success = "/create" in self.driver.current_url.lower()
            self._report_result("Create Link Navigates to /create Page", success, f"Current URL: {self.driver.current_url}")
            self.assertTrue(success)
        except TimeoutException:
            self._report_result("Create Link Navigates to /create Page", False, f"Timeout: Did not redirect to /create. Current URL: {self.driver.current_url}")
            self.fail("Navigation to /create failed.")
            
    # --- TEST 08: Login Fails with Invalid Credentials ---
    def test_08_login_fails_invalid_credentials(self):
        
        WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located(self.USERNAME_FIELD_LOCATOR)).send_keys(INVALID_USERNAME)
        self.driver.find_element(*self.PASSWORD_FIELD_LOCATOR).send_keys(INVALID_PASSWORD)
        self.driver.find_element(*self.LOGIN_BUTTON_LOCATOR).click()
        
        try:
            error_message = WebDriverWait(self.driver, TIMEOUT).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE_LOCATOR)
            )
            success = error_message.is_displayed()
            message = f"Found error message: {error_message.text}"
            
            self._report_result("Login Fails with Invalid Username and Password", success, message)
        except TimeoutException:
            current_url = self.driver.current_url.lower().rstrip('/')
            success = current_url == YOUFACE_LOGIN_URL.lower().rstrip('/')
            message = "No explicit error element found, but remained on login page."
            
            self._report_result("Login Fails with Invalid Username and Password", success, message)
        self.assertTrue(success)


if __name__ == '__main__': 
    # Set the verbosity to 0 to minimize the default unittest output (it will still print the OK/FAIL line)
    # Removing buffer=True allows the individual prints to show up immediately.
    unittest.main(exit=False, verbosity=0)
