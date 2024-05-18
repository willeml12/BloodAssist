from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:5000/")
driver.maximize_window()
time.sleep(10)

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
wait = WebDriverWait(driver, 30)
blood_type_select = wait.until(EC.presence_of_element_located((By.ID, 'blood-type')))

# Select the blood type
select = Select(blood_type_select)
select.select_by_value('O+')  
time.sleep(1)

password1 = driver.find_element(By.ID, "register-password")
password1.send_keys("Pass")
time.sleep(1)

password2 = driver.find_element(By.ID, "confirm-password")
password2.send_keys("Pass")
time.sleep(1)

register_btn = driver.find_element(By.ID,"register-button")
ActionChains(driver).scroll_to_element(register_btn).perform()
register_btn.click()
time.sleep(4)

#Find the Assessmenr title and assert it’s visibility
login_title = driver.find_element(By.TAG_NAME, 'title')
#assert login_title.is_displayed()

password1 = driver.find_element(By.ID, "dob")
password1.send_keys("05/04/1990")
time.sleep(1)

blood_type_select = wait.until(EC.presence_of_element_located((By.ID, 'btype')))
blood_type_select.click()

select = Select(blood_type_select)
select.select_by_value('O+')  
time.sleep(1)

gender_select = wait.until(EC.presence_of_element_located((By.ID, 'gender')))
gender_select.click()

select = Select(gender_select)
select.select_by_value('female')  
time.sleep(1)

gender_question = wait.until(EC.presence_of_element_located((By.ID, 'femaleQuestions')))
radio_button = driver.find_element(By.ID, "button-not-pregnant")
radio_button.click()
time.sleep(2)

password1 = driver.find_element(By.ID, "weight")
password1.send_keys("55")
time.sleep(1)

radio_button = driver.find_element(By.ID, "blood-no")
radio_button.click()
time.sleep(2)

endo_button = driver.find_element(By.ID, "endo-no")
ActionChains(driver).scroll_to_element(endo_button).perform()
wait.until(EC.presence_of_element_located((By.ID, 'endo-no')))


radio_button = driver.find_element(By.ID, "travel-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "fever-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "med-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "vaccine-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "dentist-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "pierce-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "drugs-no")
radio_button.click()
time.sleep(2)
submit_button = driver.find_element(By.ID, "submit")
ActionChains(driver).scroll_to_element(submit_button).perform()
wait.until(EC.presence_of_element_located((By.ID, 'submit')))

radio_button = driver.find_element(By.ID, "sex-no")
radio_button.click()
time.sleep(2)

radio_button = driver.find_element(By.ID, "uk-stay-no")
radio_button.click()
time.sleep(2)

endo_button = driver.find_element(By.ID, "endo-no")
ActionChains(driver).scroll_to_element(endo_button).perform()
endo_button.click()
time.sleep(2)
submit_button.click()
time.sleep(2)
home_button = driver.find_element(By.ID, "home-btn")
home_button.click()
time.sleep(5)

login_btn = driver.find_element(by=By.ID,value="login-button")
login_btn.click()
time.sleep(2)

email = driver.find_element(By.ID, "user-email")
email.send_keys("faraharoud410@gmail.com")
time.sleep(1)

password1 = driver.find_element(By.ID, "password")
password1.send_keys("Pass")
time.sleep(1)

login_btn = driver.find_element(by=By.ID,value="login-button")
login_btn.click()
time.sleep(1.5)
driver.switch_to.alert.accept()
time.sleep(10)


driver.quit()