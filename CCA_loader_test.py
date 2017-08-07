from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#testing 10-75 promotions
usr = 'cutedog@xyz123.com'
passwd = '35Paxton'
outlet = "2288416"

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get("https://myccadevau-promo.aus.ccamatil.com/")
#driver.maximize_window()

driver.get("https://myccadevau-promo.aus.ccamatil.com/login")

'''
element = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located((By.ID, 'loginLink'))
)
'''

element = driver.find_element_by_id("Username")
element.send_keys(usr)
element = driver.find_element_by_id("Password")
element.send_keys(passwd)
driver.find_element_by_id("signInButton").click()
driver.find_element_by_class_name("dropdown-toggle").click()
driver.find_element_by_link_text("Switch outlet").click()
element = driver.find_element_by_class("form-control")
element.send_keys(
#driver.quit()

#wait = WebDriverWait(driver, 10)
#element = wait.until(EC.presence_of_element_located((By.ID, 'loginLink')))
#element = driver.find_element_by_partial_link_text('Sign')

#element = driver.find_element_by_id('loginLink')
#element.click()