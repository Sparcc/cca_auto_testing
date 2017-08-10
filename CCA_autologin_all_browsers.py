from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, getopt

#testing 10-75 promotions
usr = {'promo-9193': 'cutedog@xyz123.com',
		'promo-80': 'myccatest123@gmail.com',
		'cds': 'abcdxyz@outlook.com'
		};
passwd = {'promo-9193': '35Paxton',
		'promo-80': 'Mycca@11',
		'cds': 'Mycca@11'
		};
outlet = {'promo-9193': '2288416',
		'promo-80': '2743206',
		'cds-80': '5101222',
		'cds-9193': '5116821'
		};

driver_paths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\MicrosoftWebDriver.exe'
		};

#DEFAULTS
#turn multi-browser login on/off
singleBrowser = True
selectOutlet = False
designatedBrowser = 'chrome'
usrCurrent=usr['cds']
passwdCurrent=passwd['cds']

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

#ARGUMENT HANDLING
print (argv[0])
'''
try:
	opts, args = getopt.getopt(argv,"s",["single"])
except getopt.GetoptError:
	print (argv[0], '-s')
      sys.exit(2)
	  
for opt, arg in opts:
	if opt in ('-s', '--single'):
		singleBrowser = False
'''

if singleBrowser:
	if designatedBrowser == 'chrome':
		drivers=[webdriver.Chrome(driver_paths['Chrome'])];
	if designatedBrowser == 'edge':
		drivers=[webdriver.Edge(driver_paths['Edge'])]
	if designatedBrowser == 'firefox':
		drivers=[webdriver.Firefox()]
else:
	drivers=[webdriver.Firefox(profile),
		webdriver.Chrome(driver_paths['Chrome']),
		webdriver.Edge(driver_paths['Edge'])
		];

'''
drivers=[webdriver.Firefox()
		];
'''
		
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

	element = driver.find_element_by_id("Username")
	element.send_keys(usrCurrent)
	element = driver.find_element_by_id("Password")
	element.send_keys(passwdCurrent)
	driver.find_element_by_id("signInButton").click()
	
	'''
	if selectOutlet:
		driver.find_element_by_class_name("showmyprofileddl").click()
		driver.find_element_by_link_text("Switch outlet").click()
		driver.find_element_by_class_name("search").send_keys(outlet)
		driver.find_element_by_xpath('//*[@id="outletList"]/div/div/img').click()
	'''

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