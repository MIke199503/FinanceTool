#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：QueryView.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 10:07 AM 
"""

import tkinter
from tkinter import ttk
from ComBoPicker import Combopicker
from DataModule import BasicMessage


class QueryView:
    def __init__(self, root_page):
        self.company_combo = None
        self.date_combo = None
        self.root = root_page

        self.basic_frame = tkinter.Frame(self.root, width=1920, height=1080)
        self.basic_frame.pack()

        self.choose_frame = tkinter.Frame(self.basic_frame, width=640)
        self.choose_frame.grid(row=1, column=1)

        self.tree_frame = ttk.Frame(self.basic_frame, width=640)
        self.tree_frame.grid(row=1, column=2)

        self.label2 = ttk.Label(self.tree_frame, text="No.2")
        self.label2.pack()

        self.export_frame = ttk.Frame(self.basic_frame, width=640)
        self.export_frame.grid(row=1, column=3)

        self.label3 = ttk.Label(self.export_frame, text="No.3")
        self.label3.pack()

        self.create_choose_item()

    def create_choose_item(self):
        time_label = ttk.Label(self.choose_frame, text="请选择日期")
        time_label.grid(row=1, column=1)

        self.date_combo = Combopicker(self.choose_frame, values=["全选", "2201", "2202", "2203"])
        self.date_combo.grid(row=1, column=2)

        company_label = ttk.Label(self.choose_frame, text="请选择公司")
        company_label.grid(row=2, column=1)
        _data = list(BasicMessage.company_abbreviation.keys())
        _data.insert(0, "全选")
        self.company_combo = Combopicker(self.choose_frame, values=_data)
        self.company_combo.grid(row=2, column=2)

        test_button = ttk.Button(self.choose_frame, text="getvalues", command=self.pri)
        test_button.grid(row=4, column=1, columnspan=2)

    def pri(self):
        print(self.date_combo.get())
        print(self.company_combo.get())

    def create_tree_view(self):
        pass


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("1920x1080")
    QueryView(root_page=root)
    root.mainloop()
