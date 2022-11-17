#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：ChooseFile.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 9:03 AM 
"""
import os.path
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
        self.root.geometry("1900x1000")

        self.page = ttk.Frame(self.root, width=1900, height=1000)
        self.page.place(relx=0, rely=0)
        s1 = ttk.Style()
        s1.configure("A.TButton", font=("TkDefaultFont", 25, "normal"))
        global img_gif
        img_gif = tkinter.PhotoImage(file=r'./theme/集团Logo.png')
        label_img = tkinter.Label(self.page)
        label_img.place(relx=0.395, rely=0.3)
        label_img.config(image=img_gif)
        button = ttk.Button(self.page,
                            text='点击你的数据源Excel',
                            width=25,
                            style="A.TButton",
                            command=self.callbacks)
        button.pack()
        button.place(relx=0.395, rely=0.55)


    def callbacks(self):
        """
        open askopenfilename for let user choose a Data.xlsx
        """
        filePath = fp.askopenfilename(title="请选择数据源Excel文件", filetypes=[("Excel文件", ".xlsx")])
        if not os.path.exists(filePath):
            showerror(title="很可惜，发生了一点错误。:", message="你所选择的文件不符合要求，请仔细核对并重新选择。No Files")
        else:
            try:
                showinfo(title="提示", message="加载数据需要一定时间，请耐心等待！")
                file_data = readExcel.FirstDeal(filepath=filePath)
            except:
                showerror(title="很可惜，发生了一点错误。:", message="你所选择的文件不符合要求，请仔细核对并重新选择。ReadError")
            else:
                self.page.destroy()  # shut down this view
                QueryView(root_page=self.root, data_resource=file_data)




