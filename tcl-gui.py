#import tkinter as tk
from tkinter import *

class App:
	counter = 0#int
	padding = 10#int
	buttonPadding = 2.5#int
	frame = 0#this widget
	master = 0#this tk
	windowsOpen = []#int
	childWindowId = {}#key:int
	windowId = 0#int
	parent = 0#App
	isRoot = False
	def __init__(self, master, isRoot, parent = 0, windowId = 0):
		#automatically stored in widget tree after destruction
		self.frame = Frame(master)
		self.frame.config(padx = self.padding)
		self.frame.config(pady = self.padding/2)
		self.frame.pack()
		self.master = master
		self.createElements()
		self.windowId = windowId
		self.master.protocol('WM_DELETE_WINDOW', self.closeWindow)
		self.isRoot = isRoot
	def closeWindow(self):
		print('closing window')
		if self.isRoot:
			try:
				parent.remove(self.windowId)
			except:
				print('no parent of class App')
		self.master.destroy()
		
	def createElements(self):
		print("There are no elements on this frame")
		
	def assignChildWindowId(self, key, id):
		self.childWindowId[key] = id
		
	def openWindow(self, key):
		canOpen = True
		
		for id in self.windowsOpen:
			if id == self.childWindowId[key]:
				canOpen = False
		if canOpen:
			self.windowsOpen.append(self.childWindowId[key])
			window = Tk()
			
			self.constructWindow(window,key)
			window.mainloop()
	def constructWindow(self, window, key):
		#newApp = SettingsWindow(window,parent=self.master,windowId=childWindowId[key])
		print('usage: <className>(master, parent, windowId)')
		print('use logic to check and build different windows of different "App" type classes based on key')
		
	
class SettingsWindow(App):
	def createElements(self):
		ops=['op1', 'op2', 'op3', 'op4']
		selectedOp = StringVar(self.master)
		
		w = OptionMenu(self.master, selectedOp, *ops
			).grid(row=0,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
			
		#todo: calc arg values
		
		args=['test1','test2','test3','test4']
		selectedArg = StringVar(self.master)
		
		w = OptionMenu(self.master, selectedArg, *args
			).grid(row=0,column=1, padx=self.buttonPadding, pady=self.buttonPadding)
		
		button = Button(
			self.frame, text="Add Option", command=self.addOption
			).grid(row=0,column=2, padx=self.buttonPadding, pady=self.buttonPadding)
			
		button = Button(
			self.frame, text="Save", fg="green", command=self.saveSettings
			).grid(row=10,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
	def saveSettings(self):
		print("settings have been saved")
		
	def addOption(self):
		print("options have been saved")

class MainApp(App):
	def createElements(self):
		button = Button(self.frame, text="Run", command=self.runCommand
			).grid(row=0,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
		button = Button(self.frame, text="Settings", command= lambda: self.openWindow('settings')
			).grid(row=1,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
		button = Button(
			self.frame, text="QUIT", fg="red", command=self.closeWindow
			).grid(row=10,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		
	def runCommand(self):
		print("command has been run")
	
	def constructWindow(self, window, key):
		if key == 'settings':
			newApp = SettingsWindow(window,False,parent=self.master,windowId=self.childWindowId[key])
		else:
			print('window not found, cannot open')

root = Tk()
app = MainApp(root, True)
app.assignChildWindowId('settings', 0)
root.mainloop()
#root.destroy() # optional; see description below