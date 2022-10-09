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
        """
        三分布局，三个Frame，打底
        :param root_page:父级视图
        """
        self.project_combo = None
        self.company_combo = None
        self.date_combo = None

        self.root = root_page  # 父级视图

        # 加个底
        self.basic_frame = tkinter.Frame(self.root, width=1920, height=1080, background="white")
        self.basic_frame.grid_rowconfigure(0, weight=1, minsize=self.basic_frame.winfo_reqheight())
        self.basic_frame.grid_columnconfigure(0, weight=1, minsize=self.basic_frame.winfo_reqwidth() / 3)
        self.basic_frame.grid_columnconfigure(1, weight=1, minsize=self.basic_frame.winfo_reqwidth() / 3)
        self.basic_frame.grid_columnconfigure(2, weight=1, minsize=self.basic_frame.winfo_reqwidth() / 3)
        self.basic_frame.place(relx=0, rely=0)

        # 选项视图
        self.choose_frame = tkinter.Frame(self.basic_frame, background="white")
        self.choose_frame.grid_columnconfigure(0, weight=1, minsize=self.choose_frame.winfo_reqwidth() / 3)
        self.choose_frame.grid_columnconfigure(1, weight=2, minsize=(self.choose_frame.winfo_reqwidth() * 2) / 3)
        self.choose_frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        # 表格视图
        self.tree_frame = tkinter.Frame(self.basic_frame, background="white")
        self.tree_frame.grid(row=0, column=1, sticky=tkinter.NSEW)

        # 导出视图
        self.export_frame = tkinter.Frame(self.basic_frame, background="white")
        self.export_frame.grid(row=0, column=2, sticky=tkinter.NSEW)

        # 构建详细界面
        self.create_choose_item()

    def create_choose_item(self):
        """
        构建详细的界面
        日期：Label-》ComboBox
        公司：Label-》ComboBox
        项目：Label-》ComboBox
        费用类别：Label-》New_Window
        部门：Label-》ComboBox
        :return:None
        """
        time_label = tkinter.Label(self.choose_frame, text="请选择日期：（必选）", justify="left", anchor="w", padx=2)
        time_label.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.date_combo = Combopicker(self.choose_frame, values=["全选", "2201", "2202", "2203"])
        self.date_combo.grid(row=0, column=1, sticky=tkinter.NSEW)

        company_label = tkinter.Label(self.choose_frame, text="请选择公司：（必选）", justify="left", anchor="w", padx=2)
        company_label.grid(row=1, column=0, sticky=tkinter.NSEW)

        _data = list(BasicMessage.company_abbreviation.keys())
        _data.insert(0, "全选")
        self.company_combo = Combopicker(self.choose_frame, values=_data)
        self.company_combo.grid(row=1, column=1, sticky=tkinter.NSEW)

        project_label = tkinter.Label(self.choose_frame, text="请选择项目：", justify="left", anchor="w", padx=2)
        project_label.grid(row=2, column=0, sticky=tkinter.NSEW)

        self.project_combo = Combopicker(self.choose_frame, values=["全选", "1", "2"])
        self.project_combo.grid(row=2, column=1, sticky=tkinter.NSEW)

        cost_label = tkinter.Label(self.choose_frame, text="请选择费用类别：", justify="left", anchor="w", padx=2)
        cost_label.grid(row=3, column=0, sticky=tkinter.NSEW)

        cost_button = ttk.Button(self.choose_frame, text="点击进入选择页面", command=self.choose_cost)
        cost_button.grid(row=3, column=1, sticky=tkinter.NSEW)

        depart_label = tkinter.Label(self.choose_frame, text="请选择部门：", justify="left", anchor="w", padx=2)
        depart_label.grid(row=4, column=0, sticky=tkinter.NSEW)

        depart_combo = Combopicker(self.choose_frame, values=["全选", "1", "2"])
        depart_combo.grid(row=4, column=1, sticky=tkinter.NSEW)

    def choose_cost(self):
        choose_page_basic_frame = tkinter.Frame(self.root,
                                                width=1920,
                                                height=1080,
                                                )
        choose_page_basic_frame.grid_rowconfigure(0, weight=1, minsize=choose_page_basic_frame.winfo_reqheight() / 20)
        choose_page_basic_frame.grid_rowconfigure(1, weight=18,
                                                  minsize=choose_page_basic_frame.winfo_reqheight() * 15 / 20)
        choose_page_basic_frame.grid_rowconfigure(2, weight=1,
                                                  minsize=choose_page_basic_frame.winfo_reqheight() / 20)
        choose_page_basic_frame.grid_columnconfigure(0, weight=1, minsize=choose_page_basic_frame.winfo_reqwidth() / 3)
        choose_page_basic_frame.grid_columnconfigure(1, weight=1, minsize=choose_page_basic_frame.winfo_reqwidth() / 3)
        choose_page_basic_frame.grid_columnconfigure(2, weight=1, minsize=choose_page_basic_frame.winfo_reqwidth() / 3)

        leval_1_label = tkinter.Label(choose_page_basic_frame, text="请选择一级标题",
                                      anchor="w",
                                      justify="left")
        leval_1_label.grid(row=0, column=0, sticky=tkinter.NSEW)

        var = tkinter.StringVar()
        var.set("鸡蛋 鸭蛋 鹅蛋 李狗蛋 鸡蛋 鸭蛋 鹅蛋 李狗蛋 鸡蛋 鸭蛋 鹅蛋 李狗蛋 鸡蛋 鸭蛋 鹅蛋 李狗蛋")
        leval_1_picker = tkinter.Listbox(choose_page_basic_frame, listvariable=var, selectmode="multiple")
        leval_1_picker.grid(row=1, column=0, sticky=tkinter.NSEW)

        leval_2_label = tkinter.Label(choose_page_basic_frame, text="请选择二级科目",
                                      anchor="w",
                                      justify="left")
        leval_2_label.grid(row=0, column=1, sticky=tkinter.NSEW)

        leval_2_picker = tkinter.Listbox(choose_page_basic_frame, listvariable=var, selectmode="multiple")
        leval_2_picker.grid(row=1, column=1, sticky=tkinter.NSEW)

        leval_3_label = tkinter.Label(choose_page_basic_frame, text="请选择三级科目",
                                      anchor="w",
                                      justify="left")
        leval_3_label.grid(row=0, column=2, sticky=tkinter.NSEW)

        leval_3_picker = tkinter.Listbox(choose_page_basic_frame, listvariable=var, selectmode="multiple")
        leval_3_picker.grid(row=1, column=2, sticky=tkinter.NSEW)

        ask_button = ttk.Button(choose_page_basic_frame, text="确认", command=choose_page_basic_frame.destroy, width=20,
                                )
        ask_button.grid(row=2, column=2)

        choose_page_basic_frame.place(relx=0, rely=0)

    def pri(self):
        print(self.date_combo.get())
        print(self.company_combo.get())

    def create_tree_view(self):
        pass


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("1920x1080")
    root.configure(background="white")
    root.resizable = False
    QueryView(root_page=root)
    root.mainloop()
