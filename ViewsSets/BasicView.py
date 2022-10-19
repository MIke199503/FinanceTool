#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：BasicView.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 9:19 AM 
"""
import tkinter
import os
import ChooseFile


root = tkinter.Tk()
root.geometry("1920x900")
root.title('财务')
dir_path = os.path.dirname(os.path.realpath(__file__))
root.tk.call('source', os.path.join(dir_path, 'sun-valley.tcl'))
root.tk.call("set_theme", "light")
root.configure(bg='white')
ChooseFile.ChooseFile(root=root)
root.mainloop()
