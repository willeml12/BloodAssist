from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:5000/")
#Maximizing window
driver.maximize_window()

time.sleep(1)

login_btn = driver.find_element(by=By.ID,value="login-button")
login_btn.click()

time.sleep(1)
#Find the Login title and assert it’s visibility
login_title = driver.find_element(By.TAG_NAME, 'h1')
#assert login_title.is_displayed()

register_link = driver.find_element(By.LINK_TEXT, 'Register')
register_link.click()
time.sleep(1)

#Fill registration form
first_name = driver.find_element(By.ID, "first-name")
first_name.send_keys("Farah")
time.sleep(1)
last_name = driver.find_element(By.ID, "last-name")
last_name.send_keys("Aroud")
time.sleep(1)
dob = driver.find_element(By.ID, "dob")
dob.send_keys("05/04/1990")
time.sleep(1)
email = driver.find_element(By.ID, "register-email")
email.send_keys("faraharoud410@gmail.com")
time.sleep(1)

# Wait until the blood type select element is present
wait = WebDriverWait(driver, 10)
blood_type_select = wait.until(EC.presence_of_element_located((By.ID, 'blood-type')))

# Select the blood type
select = Select(blood_type_select)
select.select_by_value('O+')  # Select the desired blood type


time.sleep(1)
driver.execute_script("window.scrollTo(0, 650)")
password1 = driver.find_element(By.ID, "register-password")
password1.send_keys("Pass")
time.sleep(1)

password2 = driver.find_element(By.ID, "confirm-password")
password2.send_keys("Pass")
time.sleep(1)
register_btn = driver.find_element(By.ID,"register-button")
register_btn.click()
time.sleep(10)

driver.quit()