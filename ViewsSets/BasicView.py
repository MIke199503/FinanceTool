#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：BasicView.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 9:19 AM 
"""
import tkinter
from tkinter import ttk
import os
import sys

sys.path.append(os.getcwd())
sys.path.append("..")
sys.path.append(".")
sys.path.append(os.getcwd().split("ViewsSets")[0])


import ChooseFile

root = tkinter.Tk()
root.geometry("1920x900")
root.title('财务')
root.tk.call('source', './forest-light.tcl')
ttk.Style().theme_use("forest-light")
s = ttk.Style()
s.configure("TLabel", padx=5)
a = ChooseFile.ChooseFile(root=root)
root.mainloop()
