import sys,os
from tkinter import *
sys.path.append(os.getcwd())
from tclApp import App
import configparser
import shlex, subprocess

class MainApp(App):
	def createElements(self):
		button = Button(self.frame, text="Run", command=self.runCommand
			).grid(row=0,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
			
		button = Button(self.frame, text="Edit Configuration", command=self.runConfig
			).grid(row=0,column=1, padx=self.buttonPadding, pady=self.buttonPadding)	
		
		button = Button(self.frame, text="Settings", command= lambda: self.openWindow('settings')
			).grid(row=1,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
		button = Button(
			self.frame, text="QUIT", fg="red", command=self.closeWindow
			).grid(row=10,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
	def runCommand(self):
		config = configparser.ConfigParser()
		config.read('config.ini')		
		args =  config['DEFAULT']['args1']
		i=0
		numInstances = int(config['DEFAULT']['numInstances'])
		while i< numInstances:
			p = subprocess.Popen('python CCA_autologin.py ' + config['DEFAULT']['args'+str(i+1)])
			i+=1
		print("command has been run")
		
	def runConfig(self):
		p = subprocess.Popen('notepad config.ini')
		
	def constructWindow(self, window, key):
		if key == 'settings':
			newApp = SettingsWindow(window,False,parent=self,windowId=self.childWindowId[key])
		else:
			print('window not found, cannot open')
			
class SettingsWindow(App):
	args=4
	argsOptionsValues =[][][]
	def createElements(self):
		for x in range(0,self.args):
			self.addArg(x)
			
		button = Button(
			self.frame, text="Add Arg", command=self.saveSettings
			).grid(row=10,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
			
		button = Button(
			self.frame, text="Save", fg="green", command=self.saveSettings
			).grid(row=10,column=1, padx=self.buttonPadding, pady=self.buttonPadding)
	
	def addArg(self, argRow):
		w = Label(self.frame, text="Arg: " + str(argRow)
			).grid(row=0+argRow,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
	
		ops=['op1', 'op2', 'op3', 'op4']
		selectedOp = StringVar(self.frame)
		
		w = OptionMenu(self.frame, selectedOp, *ops
			).grid(row=0+argRow,column=1, padx=self.buttonPadding, pady=self.buttonPadding)
		#todo: calc arg values
		
		args=['test1','test2','test3','test4']
		selectedArg = StringVar(self.master)
		
		w = OptionMenu(self.frame, selectedArg, *args
			).grid(row=0+argRow,column=2, padx=self.buttonPadding, pady=self.buttonPadding)
		
		button = Button(
			self.frame, text="Add Option", command=self.addOption
			).grid(row=0+argRow,column=999, padx=self.buttonPadding, pady=self.buttonPadding)
		
	def saveSettings(self):
		print("settings have been saved")
		
	def addOption(self):
		print("options have been saved")