from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, getopt
import os
import sqlite3
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

"""
@author: Thomas Rea
@company: RXP Services
"""

#test data
print('\nloading test data...')
user = {}
password = {}
outlet = {}
requires = {}
conn = sqlite3.connect('../db/cca_test_data.db')
c = conn.cursor()

#run -r or --restore option after getting a fresh commit
#this should only happen before dump is created otherwise
#old database will be read, dumped, then restored from dump
#and new database sql commit won't be executed
def restoreDb():
	#restore database and delete all tables
	print('\nDeleting tables before restore')
	sql = 'DROP TABLE IF EXISTS user;'
	c.executescript(sql)
	sql = 'DROP TABLE IF EXISTS outlet;'
	c.executescript(sql)
	#fill database with backup
	print('\nRestoring database')
	f = open('db.sql','r') #read
	sql = f.read()
	c.executescript(sql)
	
def dumpDb():
	with open('db.sql', 'w') as f: #write
		for line in conn.iterdump():
			f.write('%s\n' % line)	

def readDb():
	#load database to memory
	try:
		for row in c.execute('SELECT alias, username, password FROM user'):
			user[row[0]] = row[1]
			password[row[0]] = row[2]
		for row in c.execute('SELECT alias, number FROM outlet'):
			outlet[row[0]] = row[1]
		for row in c.execute('SELECT alias, userAlias FROM outlet'):
			requires[row[0]] = row[1]
	except sqlite3.OperationalError as e:
		print('OperationError!')

#always read the database - It should also always exist inititally only	
readDb()	

driverPaths = {'Chrome': 'C:\Selenium\chromedriver.exe',
		'Edge': 'C:\Selenium\MicrosoftWebDriver.exe',
		'IE': 'C:\Selenium\IEDriverServer.exe'};

#DEFAULTS
singleBrowser = False #launch single browser
selectOutlet = False #enables outlet selection
designatedBrowser = 'chrome' #default browser in single browser mode
designatedOutlet = '' #default outlet when outlet selection enabled
designatedUser = user['admin-bde'] #default user is one that tests cds system
passwordCurrent = password['admin-bde'] #default password is for user that tests cds system
testServerBaseURL = 'https://myccadevau-promo.aus.ccamatil.com' #promo dev is default environment
runDrivers = True #enables automation
acceptCommands = True #allows the use of commands to control drivers after automation has completed
drivers = [] #initial list of drivers
debugging = False
clear = "\n" * 100 #screen clearer
makeOrder = False
dbDumped = False
numberOfOrders = 1

#setting driver options
#profile = webdriver.FirefoxProfile()
#profile.accept_untrusted_certs = True
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#HOW DO I GET CAPABILITIES TO WORK??
#cannot set desired capabilities of IE for reason (registry problem??)
ieCap = DesiredCapabilities.INTERNETEXPLORER.copy()
ieCap['ignoreProtectedModeSettings'] = True
firefoxCap = DesiredCapabilities.FIREFOX.copy()
firefoxCap['acceptInsecureCerts'] = True

'''
drivers=[webdriver.Chrome(driverPaths['Chrome']),
		webdriver.Firefox(),
		webdriver.Edge(driverPaths['Edge']),
		webdriver.Ie(driverPaths['IE'])
		];
'''

#ARGUMENT HANDLING
print('getting arguments...')
options = 's:o:Su:d:i'
longOptions = ['use=','outlet=','single','user=','std','stdq','direct_outlet=','info','order=','restore','dump','debug','no_command']
try:
	opts, args = getopt.getopt(sys.argv[1:],options,longOptions)
except getopt.GetoptError as e:
	print (str(e))
	print ('General Usage: ', sys.argv[0], '<-option(single)> <--long_option')
	print ('Use -i option for more usage guides and lists of test data')
	sys.exit(2)
	
for opt, arg in opts:
	if (opt == '-s') or (opt == '--use'):
		singleBrowser = True
		designatedBrowser = arg
		print('Now in single browser testing mode')
		print('designatedBrowser is: ', designatedBrowser)
	if (opt == '-S') or (opt == '--single'):
		singleBrowser = True
	if (opt == '-u') or (opt ==  '--user'):
		designatedUser = user[arg]
		passwordCurrent = password[arg]
	if (opt == '-o') or (opt == '--outlet'):
		selectOutlet = True
		designatedOutlet = arg
	if opt == '--std':
		testServerBaseURL = 'https://myccadevau.aus.ccamatil.com'
		print('Using standard dev server...warning! xpaths might be different.')
	elif opt == '--stdq':
		testServerBaseURL = 'https://test.mycca.com.au'
		print('Using standard q server...warning! xpaths might be different.')
	if opt == '--direct_outlet': #-s option matches the --dump option as well probably
		print('Using direct outlet...')
		selectOutlet = True
		outlet['custom'] = arg
		designatedOutlet = 'custom'
	if opt == '--restore':
		print('Restoring database...')
		runDrivers = False
		acceptCommands = False
		restoreDb()
	if opt == '--dump':
		print('Dumping database...')
		runDrivers = False
		acceptCommands = False
		readDb()
		dumpDb()
		dbDumped = True
	if (opt == '-i') or (opt == '--info'):
		runDrivers = False
		acceptCommands = False
		print('------------------------------------------------------')
		print('Options available: (e.g. -s Chrome or -S <---(Chrome is designatedBrowser by default):')
		print(options)
		print('\nLong options available (e.g. --single or --use Chrome):')
		print(longOptions)
		print('\ncurrent test users (password is entered automatically): ')
		for u in user:
			print(u, ' --> ', user[u])
		print('\nFor use of outlet number directly use -d or --direct_outlet options.')
		print('Outlets available:')
		for o in outlet:
			print(o, ' --> ', outlet[o])
		print('\noutlet to user requirements:')
		for r in requires:
			print(r, ' --> ', requires[r])
	if opt == '--order':
		makeOrder = True
		numberOfOrders = arg
	if opt == '--debug':
		runDrivers = False
		acceptCommands = False
		debugging = True
	if opt == '--no_command':
		acceptCommands = False
if debugging:
	print('opt: ', opts)
	print('args: ', args)
#db still needed for restore option
#database backup
if (not dbDumped):
	dumpDb()		
conn.close()			
			
#debug output statements
#print('outlet: ',outlet)
#print('designatedOutlet: ',designatedOutlet)
print('\nFinished getting arguments...')
if (not singleBrowser and designatedOutlet !=''):
	print('Warning! multi-browser mode is unstable for outlet selection. Use Chrome or IE instead')
if runDrivers == True:	
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
		drivers=[webdriver.Firefox(),
			webdriver.Chrome(driverPaths['Chrome']),
			webdriver.Edge(driverPaths['Edge']),
			webdriver.Ie(driverPaths['IE'])
			];
			
def orderItems(driver,testServerBaseURL,numberOfOrders):
	print('Ordering ', numberOfOrders, ' items...')
	i = 0
	while i < numberOfOrders + 1:
		#ordering
		driver.get(testServerBaseURL + '/search?SearchString=390')
		#xpath='//div[@data-material-number="957601"]/span[@class="searchPage-count-control increaseQuantity"]'
		xpath='//*[@id="search"]/div[3]/div[2]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/footer[1]/div/button[2]'
		driver.find_element_by_xpath(xpath).click() #add quantity
		#xpath='//div[@data-material-number="957601"]/div/span[@class="ctrl-text"]'
		xpath='//*[@id="search"]/div[3]/div[2]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/footer[1]/button'
		driver.find_element_by_xpath(xpath).click() #add to cart
		driver.get(testServerBaseURL + '/checkout')
		xpath='//span[@class="submit"]'
		driver.find_element_by_xpath(xpath).click()
		i=i+1
			
def navigateOutlet(driver,designatedOutlet):
	try:
		print('\nSelecting an outlet....')
		#xpath='//a[@class="dropdown-toggle showmyprofileddl"]'
		xpath='//*[@id="wrapper"]/header/div[1]/nav/div/div[5]/ul/li[2]/a'
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, xpath)))
		element.click()#wait for profile dropdwon to load and click
		driver.find_element_by_link_text("Switch outlet").click()
		driver.find_element_by_class_name("search").send_keys(outlet[designatedOutlet])
		driver.implicitly_wait(10)#wait for outlet to load
		time.sleep(2)#wait for more search results appear
		try:
			xpath='//div[@data-outlet-number="'+outlet[designatedOutlet]+'-1"]/div/img'
			driver.find_element_by_xpath(xpath).click()
		except:
			xpath='//div[@data-outlet-number="'+outlet[designatedOutlet]+'-2"]/div/img'
			driver.find_element_by_xpath(xpath).click()
	except:
		print('Cannot select outlet!')
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
	element.send_keys(designatedUser)
	element = driver.find_element_by_id("Password")
	element.send_keys(passwordCurrent)
	driver.find_element_by_id("signInButton").click()
	
	
	numberOfOrders = int(numberOfOrders)
	if makeOrder:
		orderItems(driver,testServerBaseURL,numberOfOrders)
	
	if selectOutlet:
		navigateOutlet(driver,designatedOutlet)
		
while acceptCommands:
	print('Please enter a command:')
	command = input()
	if 'quit' == command.lower():
		for driver in drivers:
			driver.quit()
		acceptCommands = False
	if 'running' == command.lower():
		for driver in drivers:
			print(driver.name)
	if ('release') == command.lower():
		acceptCommands = False
		print('Drivers are still running but script is ending')
	if 'outlet' == command.lower():
		print('Input designated outlet: ')
		cArg = input()
		designatedOutlet = cArg
		for driver in drivers:
			navigateOutlet(driver, designatedOutlet)
	if 'direct_outlet' == command.lower():
		print('Input direct outlet: ')
		cArg = input()
		designatedOutlet = cArg
		outlet['custom'] = cArg
		designatedOutlet = 'custom'
		for driver in drivers:
			navigateOutlet(driver,designatedOutlet)
	if 'order' == command.lower():
		print('Input number to order: ')
		cArg = input()
		for driver in drivers:
			orderItems(driver,testServerBaseURL,int(cArg))
		
print('\nProgram quiting...\n')