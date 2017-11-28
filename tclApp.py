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
		self.parent = parent
	def closeWindow(self):
		print('closing window')
		#before destroy free up list
		if not self.isRoot:
			print('this is not a root widget')
			self.parent.windowsOpen.remove(self.windowId)
			#print(self.parent.windowsOpen)
		self.master.destroy()
		
	def createElements(self):
		print("There are no elements on this frame")
		
	def assignChildWindowId(self, key, id):
		self.childWindowId[key] = id
		
	def openWindow(self, key):
		canOpen = True
		print('self.childWindowId[key]'+str(self.childWindowId[key]))
		for id in self.windowsOpen:
			if id == self.childWindowId[key]:
				canOpen = False
				print('cannot open, window is already opened!')
		if canOpen:
			self.windowsOpen.append(self.childWindowId[key])
			window = Tk()
			
			self.constructWindow(window,key)
			window.mainloop()
	def constructWindow(self, window, key):
		#newApp = SettingsWindow(window,parent=self.master,windowId=childWindowId[key])
		print('usage: <className>(master, parent, windowId)')
		print('use logic to check and build different windows of different "App" type classes based on key')