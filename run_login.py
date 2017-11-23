import sys
import os
import configparser
import shlex, subprocess

#window logic goes here

config = configparser.ConfigParser()
config.read('config.ini')		
args =  config['DEFAULT']['args1']
i=0
numInstances = int(config['DEFAULT']['numInstances'])
while i< numInstances:
	p = subprocess.Popen('python CCA_autologin.py ' + config['DEFAULT']['args'+str(i+1)])
	i+=1