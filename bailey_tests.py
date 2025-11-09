from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# don't specify chromedriver path; GitHub runner already has it
driver = webdriver.Chrome(options=options)

def find_required(by, value, desc):
    """
    Try to find an element. If it's not there, print a FAILED line
    but don't crash the whole test. Returns the element or None.
    """
    try:
        el = driver.find_element(by, value)
        return el
    except NoSuchElementException:
        print(f"[FAILED] - {desc} not found (selector: {value})")
        return None

try:
    driver.get("http://127.0.0.1:5000/")
    time.sleep(2)
    print("--= Beginning Tests =--")

    # 1) Title contains 'CampusTalk'
    title = driver.title
    if "CampusTalk" in title:
        print("[PASSED] - Title contains 'CampusTalk'")
    else:
        print(f"[FAILED] - Unexpected title: '{title}'")

    # 2) Card header text is 'Login'
    header = find_required(By.CSS_SELECTOR, ".card .card-title", "Card header (.card .card-title)")
    if header:
        if header.text.strip().lower() == "login":
            print("[PASSED] - Card header is 'Login'")
        else:
            print(f"[FAILED] - Card header text incorrect: '{header.text.strip()}'")

    # 3) Username input present & enabled
    username = find_required(By.NAME, "username", "Username input")
    if username:
        if username.is_displayed() and username.is_enabled():
            print("[PASSED] - Username input visible & enabled")
        else:
            print("[FAILED] - Username input missing or disabled")

        if (username.get_attribute("type") or "") == "text":
            print("[PASSED] - Username input type is 'text'")
        else:
            print("[FAILED] - Username input type incorrect")

    # 4) Password input present, masked & enabled
    password = find_required(By.NAME, "password", "Password input")
    if password:
        if password.is_displayed() and password.is_enabled():
            print("[PASSED] - Password input visible & enabled")
        else:
            print("[FAILED] - Password input missing or disabled")

        if (password.get_attribute("type") or "") == "password":
            print("[PASSED] - Password input is masked (type='password')")
        else:
            print("[FAILED] - Password input not masked")

    # 5) Login button visible/enabled & primary class
    login_btn = find_required(
        By.CSS_SELECTOR,
        "input[type='submit'][value='Login']",
        "Login button"
    )
    if login_btn:
        login_classes = (login_btn.get_attribute("class") or "")
        if login_btn.is_displayed() and login_btn.is_enabled():
            print("[PASSED] - Login button visible & enabled")
        else:
            print("[FAILED] - Login button missing or disabled")

        if "btn" in login_classes and "btn-primary" in login_classes:
            print("[PASSED] - Login button has Bootstrap primary classes")
        else:
            print(f"[FAILED] - Login button classes incorrect: {login_classes}")

    # 6) Create button visible/enabled & success class
    create_btn = find_required(
        By.CSS_SELECTOR,
        "input[type='submit'][value='Create']",
        "Create button"
    )
    if create_btn:
        create_classes = (create_btn.get_attribute("class") or "")
        if create_btn.is_displayed() and create_btn.is_enabled():
            print("[PASSED] - Create button visible & enabled")
        else:
            print("[FAILED] - Create button missing or disabled")

        if "btn" in create_classes and "btn-success" in create_classes:
            print("[PASSED] - Create button has Bootstrap success classes")
        else:
            print(f"[FAILED] - Create button classes incorrect: {create_classes}")

    # 7) Form method/action check
    form = find_required(By.TAG_NAME, "form", "Login form")
    if form:
        method = (form.get_attribute("method") or "").lower()
        action = (form.get_attribute("action") or "")

        if method == "post":
            print("[PASSED] - Form method is POST")
        else:
            print(f"[FAILED] - Form method incorrect: {method}")

        if action.endswith("/login"):
            print("[PASSED] - Form action ends with /login")
        else:
            print(f"[FAILED] - Form action incorrect: {action}")

    # 8) Inputs start empty
    if username:
        if (username.get_attribute("value") or "") == "":
            print("[PASSED] - Username starts empty")
        else:
            print(f"[FAILED] - Username pre-filled with '{username.get_attribute('value')}'")

    if password:
        if (password.get_attribute("value") or "") == "":
            print("[PASSED] - Password starts empty")
        else:
            print(f"[FAILED] - Password pre-filled with '{password.get_attribute('value')}'")

    # 9) Labels present for username/password
    labels = driver.find_elements(By.TAG_NAME, "label")
    label_texts = [l.text.strip().lower() for l in labels]

    if "username" in label_texts:
        print("[PASSED] - Username label present")
    else:
        print("[FAILED] - Username label missing")

    if "password" in label_texts:
        print("[PASSED] - Password label present")
    else:
        print("[FAILED] - Password label missing")

    # 10) Keyboard tab order: username -> password -> login
    # only do this if all 3 elements exist
    if username and password and login_btn:
        username.click()
        driver.switch_to.active_element.send_keys(Keys.TAB)
        active = driver.switch_to.active_element

        if active == password:
            print("[PASSED] - Tab from username focuses password")
        else:
            print("[FAILED] - Tab order incorrect (username -> ?)")

        active.send_keys(Keys.TAB)
        active = driver.switch_to.active_element

        if active == login_btn:
            print("[PASSED] - Tab from password focuses login button")
        else:
            print("[FAILED] - Second Tab did not focus login button")
    else:
        print("[INFO] - Skipping tab-order test because one of the fields/buttons was missing.")

except Exception as e:
    # keep this so we see unexpected problems
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
