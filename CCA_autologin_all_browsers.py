from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, getopt

#testing 10-75 promotions
usr = {'promo-9193': 'cutedog@xyz123.com',
		'promo-80': 'myccatest123@gmail.com',
		'cds': 'abcdxyz@outlook.com',
		'promo-1075': 'myccatest123@gmail.com',
		'webtestuser': 'webtestuser1'
		};
passwd = {'promo-9193': '35Paxton',
		'promo-80': 'Mycca@11',
		'cds': 'Mycca@11',
		'promo-1075': 'Mycca@11',
		'webtestuser': 'b'
		};
outlet = {'promo-9193': '2288416',
		'promo-80': '2743206',
		'cds-80': '5101222',
		'cds-9193': '5116821'
		};

driverPaths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\MicrosoftWebDriver.exe'
		};

#DEFAULTS
#turn multi-browser login on/off
singleBrowser = False
selectOutlet = False
designatedBrowser = 'chrome'
designatedOutlet = ''
usrCurrent=usr['webtestuser']
passwdCurrent=passwd['webtestuser']

#setting driver options
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
		
#IE does not seem to work on proxy
#https://stackoverflow.com/questions/17625047/ie-and-chrome-not-working-with-selenium2-python

'''
drivers=[webdriver.Chrome(driverPaths['Chrome']),
		webdriver.Firefox(),
		webdriver.Edge(driverPaths['Edge']),
		webdriver.Ie(driverPaths['IE'])
		];
'''

#ARGUMENT HANDLING
print('getting arguments...')
print(sys.argv)
try:
	opts, args = getopt.getopt(sys.argv[1:],"so:",['single','outlet='])
except getopt.GetoptError as e:
	print (str(e))
	print (sys.argv[0], '<option>')
	sys.exit(2)
	  
for opt, arg in opts:
	if opt in ('-s', '--single'):
		singleBrowser = True
		print('Now in single browser testing mode')
	if opt in ('-o', '--outlet'):
		designatedOutlet = arg
print('finished getting arguments')

if singleBrowser:
	if designatedBrowser == 'chrome':
		drivers=[webdriver.Chrome(driverPaths['Chrome'])];
	if designatedBrowser == 'edge':
		drivers=[webdriver.Edge(driverPaths['Edge'])]
	if designatedBrowser == 'firefox':
		drivers=[webdriver.Firefox()]
else:
	drivers=[webdriver.Firefox(profile),
		webdriver.Chrome(driverPaths['Chrome']),
		webdriver.Edge(driverPaths['Edge'])
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
	
	
	if selectOutlet:
		driver.find_element_by_class_name("showmyprofileddl").click()
		driver.find_element_by_link_text("Switch outlet").click()
		driver.find_element_by_class_name("search").send_keys(outlet[designatedOutlet])
		driver.find_element_by_xpath('//*[@id="outletList"]/div/div/img').click()
	

accept_commands = True
try:
	while accept_commands:
		
		print('Please enter a command:')
		command = input()
		if 'quit' in command.lower():
			for driver in drivers:
				driver.quit()
				accept_commands = False
		if 'running' in command:
			for driver in drivers:
				print(driver.name)
	print('Program quiting')
except:
	print('Driver no longer available, quiting...')