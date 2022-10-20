#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：BasicView.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 9:19 AM 
"""
import tkinter
import ChooseFile
from tkinter import ttk
import sys


sys.path.append("..")

root = tkinter.Tk()
root.geometry("1920x900")
root.title('财务')
root.tk.call('source', 'forest-light.tcl')
ttk.Style().theme_use("forest-light")
s = ttk.Style()
s.configure("TLabel", padx=5)
a = ChooseFile.ChooseFile(root=root)
root.mainloop()
