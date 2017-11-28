from tkinter import *
from tclGui import *

root = Tk()
app = MainApp(root, True)
app.assignChildWindowId('settings', 0)
root.mainloop()
#root.destroy() # optional; see description below