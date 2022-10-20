import tkinter
from tkinter import ttk
import os
import sys

sys.path.append(os.getcwd())

import ViewsSets.ChooseFile as choose

root = tkinter.Tk()
root.geometry("1920x900")
root.title('财务')
root.tk.call('source', './ViewsSets/forest-light.tcl')
ttk.Style().theme_use("forest-light")
s = ttk.Style()
s.configure("TLabel", padx=5)
a = choose.ChooseFile(root=root)
root.mainloop()
