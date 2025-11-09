from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://127.0.0.1:5000/")
    time.sleep(2)
    print("--= Beginning Tests =--")

    # 1. Create link/button present 
    create_links = driver.find_elements(By.XPATH, "//a[@href='/create' or contains(normalize-space(.), 'Create')]")
    if create_links:
        create = create_links[0]
        if create.is_displayed() and create.is_enabled():
            print("[PASSED] - Create link/button visible.")
        else:
            print("[FAILED] - Create link/button not interactable.")
    else:
        print("[FAILED] - Create link/button missing.")
    
    #2. Create Your Account title present

    try:
        create.click()
    except Exception:
        
        driver.get("http://127.0.0.1:5000/create")
    time.sleep(2)
    elements = driver.find_elements(By.XPATH, "//h3[contains(text(), 'Create Your Account')]")
    if elements:
        heading = elements[0]
        print("[PASSED] - Create Your Account found.")
    else:
        heading = None
        print("[FAILED] - Create Your Account missing.")

    # 3. Username input present
    username_inputs = driver.find_elements(By.NAME, 'username')
    if username_inputs:
        print("[PASSED] - Username input present.")
    else:
        print("[FAILED] - Username input missing.")

    # 4. Major input present
    major_inputs = driver.find_elements(By.NAME, 'major')
    if major_inputs:
        print("[PASSED] - Major input present.")
    else:
        print("[FAILED] - Major input missing.")

    # 5. Interests input present
    interests_inputs = driver.find_elements(By.NAME, 'interests')
    if interests_inputs:
        print("[PASSED] - Interests input present.")
    else:
        print("[FAILED] - Interests input missing.")

    # 6. Year input present
    year_inputs = driver.find_elements(By.NAME, 'year')
    if year_inputs:
        print("[PASSED] - Year input present.")
    else:
        print("[FAILED] - Year input missing.")

    # 7. Finish Setup button present
    finish_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Finish Setup')]")
    if finish_buttons:
        finish = finish_buttons[0]
        print("[PASSED] - Finish Setup button present.")
    else:
        finish = None
        print("[FAILED] - Finish Setup button missing.")

    # 8. Form uses POST
    forms = driver.find_elements(By.XPATH, "//form[@method='POST']")
    if forms:
        print("[PASSED] - Form method POST present.")
    else:
        print("[FAILED] - Form method POST missing.")

    # 9. Inputs have form-control class (at least username+major+interests)
    form_controls = driver.find_elements(By.CSS_SELECTOR, "input.form-control")
    if len(form_controls) >= 3:
        print("[PASSED] - Inputs have form-control class.")
    else:
        print("[FAILED] - form-control class missing on inputs.")

    # 10. Submitting the form redirects to the home/feed page
    if finish is not None and username_inputs:
        try:
            username_inputs[0].clear()
            username_inputs[0].send_keys('selenium_test_user')
            finish.click()
            time.sleep(2)
            home_headers = driver.find_elements(By.XPATH, "//h1[contains(text(), 'Welcome')]")
            if home_headers:
                print("[PASSED] - Submitting create form navigates to home.")
            else:
                print("[FAILED] - Submitting form did not navigate to home.")
        except Exception as e:
            print("[FAILED] - Error submitting form:", e)
    else:
        print("[SKIPPED] - Cannot test form submit (missing button or username input).")


except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
