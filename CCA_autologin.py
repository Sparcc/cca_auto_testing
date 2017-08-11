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
		'cds-9193': '5116821',
		'cds-off-fo': '1137767',
		'cds-on-fo': '5209236'
		};

driverPaths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\MicrosoftWebDriver.exe'
		};

#DEFAULTS
singleBrowser = False #launch single browser
selectOutlet = False
designatedBrowser = 'chrome'
designatedOutlet = ''
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
drivers=[webdriver.Chrome(driverPaths['Chrome']),
		webdriver.Firefox(),
		webdriver.Edge(driverPaths['Edge']),
		webdriver.Ie(driverPaths['IE'])
		];
'''

#ARGUMENT HANDLING
print('getting arguments...')
print(sys.argv)
options = 's:o:Su:'
longOptions = ['use=','outlet=','single','user=']
try:
	opts, args = getopt.getopt(sys.argv[1:],options,longOptions)
except getopt.GetoptError as e:
	print (str(e))
	print ('General Usage: ', sys.argv[0], '<option>')
	print('Options available (e.g. -s data or -S):', options)
	print('Long options available (e.g. --single or --use data):', longOptions)
	print ('current test users:')
	print ('promo-9193','promo-80','cds','promo1075','cds',sep='\n')
	sys.exit(2)
print('opt: ', opts)
print('args: ', args)	  
for opt, arg in opts:
	if opt in ('-s', '--use'):
		singleBrowser = True
		print('arg is: ', arg)
		designatedBrowser = arg
		print('Now in single browser testing mode')
		print('designatedBrowser is: ', designatedBrowser)
	if opt in ('-S', '--single'):
		singleBrowser = True
	if opt in ('-u', '--user'):
		usrCurrent=usr[arg]
		passwdCurrent=passwd[arg]
		
	if opt in ('-o', '--outlet'):
		selectOutlet = True
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
		driver.implicitly_wait(5)#edge needs to wait

	element = driver.find_element_by_id("Username")
	element.send_keys(usrCurrent)
	element = driver.find_element_by_id("Password")
	element.send_keys(passwdCurrent)
	driver.find_element_by_id("signInButton").click()
	
	
	if selectOutlet:
		print('Selecting an outlet....')
		driver.find_element_by_class_name("showmyprofileddl").click()
		driver.find_element_by_link_text("Switch outlet").click()
		driver.find_element_by_class_name("search").send_keys(outlet[designatedOutlet])
		driver.implicitly_wait(10)
		outletXpath='//div[@data-outlet-number="'+outlet[designatedOutlet]+'-1"]/div/img'
		#//*[@id="outletList"]/div[1]/div
		driver.find_element_by_xpath(outletXpath).click()
	

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
		if 'leave' in command.lower():
			accept_commands = False
			print('Drivers are still running but script is ending')
	print('Program quiting')
except:
	print('Driver no longer available, quiting...')