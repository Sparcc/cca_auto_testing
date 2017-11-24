import sys,os
from tkinter import *
sys.path.append(os.getcwd())
from tclApp import App

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
			newApp = SettingsWindow(window,False,parent=self,windowId=self.childWindowId[key])
		else:
			print('window not found, cannot open')
			
class SettingsWindow(App):
	def createElements(self):
		#ops=['op1', 'op2', 'op3', 'op4']
		#selectedOp = StringVar(self.master)
		#
		#w = OptionMenu(self.master, selectedOp, *ops
		#	).grid(row=0,column=0, padx=self.buttonPadding, pady=self.buttonPadding)
		#	
		#todo: calc arg values
		#
		#args=['test1','test2','test3','test4']
		#selectedArg = StringVar(self.master)
		#
		#w = OptionMenu(self.master, selectedArg, *args
		#	).grid(row=0,column=1, padx=self.buttonPadding, pady=self.buttonPadding)
		
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

root = Tk()
app = MainApp(root, True)
app.assignChildWindowId('settings', 0)
root.mainloop()
#root.destroy() # optional; see description below