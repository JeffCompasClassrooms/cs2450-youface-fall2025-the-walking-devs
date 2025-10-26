from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


service = Service("C:\\Users\\Pqanh\\bin\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)


print("Beginning Tests - Quoc Anh")


passed = 0
total = 10

try:
   
    driver.get("http://127.0.0.1:5005")
    time.sleep(1)
    
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("")   
    password.send_keys("")  


    login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
    login_button.click()


    time.sleep(2)

 
    assert "/login" not in driver.current_url
    print("[PASSED] - Logged in successfully (redirect occurred)")
    passed += 1

    welcome = driver.find_element(By.XPATH, "//*[contains(text(),'Welcome')]")
    assert "Welcome" in welcome.text
 

    body_text = driver.page_source
    assert "Welcome" in body_text and "!" in body_text
    print("[PASSED] - Welcome message appears")
    passed += 1

    
    new_post_label = driver.find_element(By.XPATH, "//*[contains(text(),'New Post')]")
    assert new_post_label.is_displayed()
    print("[PASSED] - 'New Post' text exists")
    passed += 1

 
    post_input = driver.find_element(By.NAME, "post")  
    assert post_input.get_attribute("value") == ""
    print("[PASSED] - New post field is empty by default")
    passed += 1

    
    my_feed = driver.find_element(By.XPATH, "//*[contains(text(),'My Feed')]")
    assert my_feed.is_displayed()
    print("[PASSED] - 'My Feed' exists")
    passed += 1

   
    post_input = driver.find_element(By.NAME, "post")  
    placeholder = post_input.get_attribute("placeholder")
    assert "What's on your mind?" in placeholder
    print("[PASSED] - Placeholder message 'What's on your mind?' exists in new post field")
    passed += 1

    
    add_friend_label = driver.find_element(By.XPATH, "//*[contains(text(),'Add Friend')]")
    assert add_friend_label.is_displayed()
    print("[PASSED] - 'Add Friend' section exists")
    passed += 1


   
    brand = driver.find_element(By.CLASS_NAME, "navbar-brand")
    assert "CampusTalk" in brand.text
    print("[PASSED] - CampusTalk brand exists")
    passed += 1

    
    logout_btn = driver.find_element(By.NAME, "logout")
    assert logout_btn.is_displayed()
    print("[PASSED] - Logout button exists")
    passed += 1

    
    assert "btn-secondary" in logout_btn.get_attribute("class")
    print("[PASSED] - Logout button is white")
    passed += 1

except Exception as e:
    print("[FAILED] -", e)

finally:
    print("\nEnding Tests:")
    print(f"{total} Tests Ran: {passed} Tests Passed")
    driver.quit()