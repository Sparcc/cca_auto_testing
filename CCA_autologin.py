from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, getopt

"""
@author: Thomas Rea
@company: RXP Services
"""

#test data
usr = {'promo-9193': 'cutedog@xyz123.com',
		'cds': 'abcdxyz@outlook.com',
		'promo-1075': 'myccatest123@gmail.com',
		'webtestuser': 'webtestuser1'
		};
passwd = {'promo-9193': '35Paxton',
		'cds': 'Mycca@11',
		'promo-1075': 'Mycca@11',
		'webtestuser': 'b'
		};
outlet = {'promo-9192-banners': '2288416', #need promo-9193
		'promo-93': '5772504',
		'promo-9293': '2156999',
		'promo-9193-coupons': '2288416',
		'promo-1030-92': '1148617', #need promo-1075
		'promo-1020-91': '5204048',
		'promo-40': '2743206',
		'promo-50': '2156416', #assortment deal - need webtestuser
		'promo-60': '2156672', #assortment deal - need webtestuser
		'promo-70': '2270933', #assortment deal - need webtestuser
		'promo-80': '2743206',
		'cds-80': '5101222', #need cds
		'cds-9193': '5116821',
		'cds-off-fo': '1137767', #need webtestuser
		'cds-on-fo': '5209236'
		};

driverPaths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\IEDriverServer.exe'
		};

#DEFAULTS
singleBrowser = False #launch single browser
selectOutlet = False
designatedBrowser = 'chrome'
designatedOutlet = ''
usrCurrent=usr['cds']
passwdCurrent=passwd['cds']
testServerBaseURL='https://myccadevau-promo.aus.ccamatil.com'
#drivers = []

#setting driver options
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#HOW DO I GET CAPABILITIES TO WORK??
#cannot set desired capabilities of IE for reason (registry problem??)
#ieCapabilities = DesiredCapabilities.INTERNETEXPLORER.copy()
#ieCapabilities['ignoreProtectedModeSettings'] = True
#firefoxCapabilities = DesiredCapabilities.FIREFOX.copy()
#firefoxCapabilities['acceptInsecureCerts'] = True

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
options = 's:o:Su:d:'
longOptions = ['use=','outlet=','single','user=','std','direct_outlet=']
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
		usrCurrent = usr[arg]
		passwdCurrent = passwd[arg]
	if opt in ('-o', '--outlet'):
		selectOutlet = True
		designatedOutlet = arg
	if opt in ('--std'):
		testServerBaseURL = 'https://myccadevau.aus.ccamatil.com'
		print('Using standard dev server...warning! xpaths might be different.')
	if opt in ('-d', '--direct_outlet'):
		outlet['custom'] = arg
		designatedOutlet = 'custom'
		
print('finished getting arguments')

if singleBrowser:
	if designatedBrowser == 'chrome':
		drivers=[webdriver.Chrome(driverPaths['Chrome'])];
	if designatedBrowser == 'edge':
		drivers=[webdriver.Edge(driverPaths['Edge'])]
	if designatedBrowser == 'firefox':
		drivers=[webdriver.Firefox()]
	if designatedBrowser == 'ie':
		drivers=[webdriver.Ie(driverPaths['IE'])]
else:
	drivers=[webdriver.Firefox(profile),
		webdriver.Chrome(driverPaths['Chrome']),
		webdriver.Edge(driverPaths['Edge']),
		webdriver.Ie(driverPaths['IE'])
		];
		
for driver in drivers:

	#Different drivers have different functions!
	#Browsers also have different behavious
	#Keep in mind driver execution order

	#driver.maximize_window()
	#driver.implicitly_wait(10)
	driver.get(testServerBaseURL)
	#driver.implicitly_wait(10)
	driver.get(testServerBaseURL+'/login')
	
	#trust untrusted cert in Edge (could use desired capabilities instead)
	if 'error' in driver.title:
		driver.find_element_by_id('moreInformationDropdownSpan').click()
		driver.find_element_by_id('invalidcert_continue').click()
		driver.implicitly_wait(5)#edge needs to wait
		
	#trust untrusted cert in IE
	if designatedBrowser == 'IE':
		WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.ID, 'invalidcert_mainTitle')))
	if 'secure' in driver.title:
		xpath='//td//span[@id="moreInfoContainer"]/a'
		driver.find_element_by_xpath(xpath).click()
		xpath='//a[@id="overridelink"]'
		driver.find_element_by_xpath(xpath).click()
		driver.implicitly_wait(5)
	
		
	element = driver.find_element_by_id("Username")
	element.send_keys(usrCurrent)
	element = driver.find_element_by_id("Password")
	element.send_keys(passwdCurrent)
	driver.find_element_by_id("signInButton").click()
	
	
	if selectOutlet:
		print('Selecting an outlet....')
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, '//a[@class="dropdown-toggle showmyprofileddl"]')))
		element.click()#wait for profile dropdwon to load and click
		#driver.find_element_by_class_name("showmyprofileddl").click()
		driver.find_element_by_link_text("Switch outlet").click()
		#element = WebDriverWait(driver, 10).until(
		#	EC.presence_of_element_located((By.LINK_TEXT, 'Switch Outlet')))
		#element.click()
		#element = WebDriverWait(driver, 10).until(
		#	EC.presence_of_element_located((By.XPATH, 'Switch Outlet')))
		#element.click()
		driver.find_element_by_class_name("search").send_keys(outlet[designatedOutlet])
		driver.implicitly_wait(10)#wait for outlet to load
		xpath='//div[@data-outlet-number="'+outlet[designatedOutlet]+'-1"]/div/img'
		#//*[@id="outletList"]/div[1]/div
		driver.find_element_by_xpath(xpath).click()
	

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
		if ('leave','release') in command.lower():
			accept_commands = False
			print('Drivers are still running but script is ending')
	print('Program quiting')
except:
	print('Driver no longer available, quiting...')