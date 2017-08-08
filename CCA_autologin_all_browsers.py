from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#login details
usr = 'abcdxyz@outlook.com'
passwd = 'Mycca@11'
outlet = '5151408'

selectOutlet = False

driver_paths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\MicrosoftWebDriver.exe'
		};

#turn multi-browser login on/off
singleBrowser = True
designatedBrowser = driver_paths['Chrome'];
#setting driver options
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
		
#IE does not seem to work on proxy
#https://stackoverflow.com/questions/17625047/ie-and-chrome-not-working-with-selenium2-python

'''
drivers=[webdriver.Chrome(driver_paths['Chrome']),
		webdriver.Firefox(),
		webdriver.Edge(driver_paths['Edge']),
		webdriver.Ie(driver_paths['IE'])
		];
'''

if singleBrowser:
	drivers=[webdriver.Chrome(designatedBrowser)];
else:
	drivers=[webdriver.Firefox(profile),
		webdriver.Chrome(driver_paths['Chrome']),
		webdriver.Edge(driver_paths['Edge'])
		];

'''
drivers=[webdriver.Ie(driver_paths['IE'])
		];
'''

#drivers[1] = webdriver.Firefox()
		
for driver in drivers:

	#Different drivers have different functions!
	#Browsers also have different behavious
	#Keep in mind driver execution order

	#driver.maximize_window()
	#driver.implicitly_wait(10)
	driver.get("https://myccadevau-promo.aus.ccamatil.com/")
	#driver.implicitly_wait(10)
	driver.get("https://myccadevau-promo.aus.ccamatil.com/login")
	
	#trust untrusted cert in Edge
	if 'error' in driver.title:
		driver.find_element_by_id('moreInformationDropdownSpan').click()
		driver.find_element_by_id('invalidcert_continue').click()
	
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
	
	if selectOutlet:
		driver.find_element_by_class_name("showmyprofileddl").click()
		driver.find_element_by_link_text("Switch outlet").click()
		driver.find_element_by_class_name("search").send_keys(outlet)
		driver.find_element_by_xpath('//*[@id="outletList"]/div/div/img').click()

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