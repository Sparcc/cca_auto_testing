from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process

#testing 10-75 promotions
usr = 'cutedog@xyz123.com'
passwd = '35Paxton'
outlet = '2288416'

#setting driver options
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

driver_paths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\MicrosoftWebDriver.exe'
		};

def driverThread(driver):
	print("Starting " + name)
	
	#Different drivers have different functions!
	#Browsers also have different behaviours
	#Keep in mind driver execution order
	
	#driver.maximize_window()
	driver.implicitly_wait(10)
	driver.get("https://myccadevau-promo.aus.ccamatil.com/")
	driver.implicitly_wait(10)
	driver.get("https://myccadevau-promo.aus.ccamatil.com/login")
	
	#trust untrusted cert in Edge
	if 'error' in driver.title:
		driver.find_element_by_id('moreInformationDropdownSpan').click()
		driver.find_element_by_id('invalidcert_continue').click()
	
	element = driver.find_element_by_id("Username")
	element.send_keys(usr)
	element = driver.find_element_by_id("Password")
	element.send_keys(passwd)
	driver.find_element_by_id("signInButton").click()
	
	print("Exiting " + name)

'''
drivers=[webdriver.Chrome(driver_paths['Chrome']),
		webdriver.Firefox(),
		webdriver.Edge(driver_paths['Edge'])
		];	
'''

drivers=[webdriver.Chrome(driver_paths['Chrome'])
		];	

i=0		
p = Process(target=driverThread, args=(drivers[i],))
p.start()
'''
p=[]
i=0
if __name__ == '__main__':
	for driver in drivers:
		p.append(Process(target=driverThread, args=(drivers[i],)))
		p[i].start()
	i=i+1
'''
		
#p = Process(target=driverThread, args=(1, 'FirefoxBrowser', webdriver.Firefox(profile),))
#p.start()
#p = Process(target=driverThread, args=(2, 'ChromeBrowser', webdriver.Chrome(driver_paths['Chrome']),))
#p.start()
#p = Process(target=driverThread(3, 'EdgeBrowser', webdriver.Edge(driver_paths['Edge']))
#p.start()

accept_commands = True
while accept_commands:
	print('please enter a command')
	command = input()
	if 'quit' in command:
		for driver in drivers:
			driver.quit()
			accept_commands = False
	if 'running' in command:
		for driver in drivers:
			print(driver.name)