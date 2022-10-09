#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：ChooseFile.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 9:03 AM 
"""
import tkinter
import tkinter.filedialog as fp
from tkinter import ttk
from tkinter.messagebox import *
import DataModule.ReadExcel as readExcel
from ViewsSets.QueryView import QueryView


class ChooseFile:
    def __init__(self, root):
        self.filepath = ""
        self.root = root
        self.root.geometry("1920x1080")

        # built views by automatic
        self.page = tkinter.Frame(self.root, width=1920, height=1080, background="white")
        self.page.place(relx=0, rely=0)
        s1 = ttk.Style()
        s1.configure("A.TButton", font=("Arial", 25, "normal"))
        button = ttk.Button(self.page,
                            text='点击你的数据源Excel',
                            width=25,
                            style="A.TButton",
                            command=self.callbacks)
        button.place(relx=0.4, rely=0.4)

    def callbacks(self):
        """
        open askopenfilename for let user choose a Data.xlsx
        """
        filePath = fp.askopenfilename(title="请选择数据源Excel文件", filetypes=[("Excel文件", ".xlsx")])

        try:
            readExcel.FirstDeal(filepath=filePath)
        except:
            showerror(title="很可惜，发生了一点错误。:", message="你所选择的文件不符合要求，请仔细核对并重新选择。")
        else:
            self.page.destroy()  # shut down this view
            QueryView(root_page=self.root)
            # start the next view ,we need resource because want to economize the internal memory.
            # it's not need to open file twice .




