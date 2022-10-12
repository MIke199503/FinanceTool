#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：QueryView.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 10:07 AM 
"""

import tkinter
from tkinter.messagebox import showerror
from tkinter import ttk
from ComBoPicker import Combopicker
from DataModule import BasicMessage
from DataModule.GetDynamicData import Dynamic_Data


class QueryView:
    def __init__(self, root_page, data_resource=None):
        """
        三分布局，三个Frame，打底
        :param root_page:父级视图
        """
        self.data_resource = data_resource

        self.dynamic = Dynamic_Data(data_resource=self.data_resource)

        self.table = None
        self.project_combo = None
        self.company_combo = None
        self.date_combo = None

        self.company_list = []

        self.root = root_page  # 父级视图

        # 加个底
        self.basic_frame = tkinter.Frame(self.root, width=1920, height=1080, background="white")
        self.basic_frame.grid_rowconfigure(0, weight=1, minsize=self.basic_frame.winfo_reqheight())
        self.basic_frame.grid_columnconfigure(0, weight=2)
        self.basic_frame.grid_columnconfigure(1, weight=4)
        self.basic_frame.grid_columnconfigure(2, weight=1, minsize=self.basic_frame.winfo_reqwidth() / 7)
        self.basic_frame.place(relx=0, rely=0)

        # 选项视图
        self.choose_frame = tkinter.Frame(self.basic_frame, background="white")
        self.choose_frame.grid_columnconfigure(0, weight=1,)
        self.choose_frame.grid_columnconfigure(1, weight=2,)
        self.choose_frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        # 表格视图
        self.tree_frame = tkinter.Frame(self.basic_frame, background="white")
        self.tree_frame.grid(row=0, column=1, sticky=tkinter.NSEW)

        # 导出视图
        self.export_frame = tkinter.Frame(self.basic_frame, background="white")
        self.export_frame.grid(row=0, column=2, sticky=tkinter.NSEW)

        # 构建详细界面
        self.create_choose_item()
        self.create_tree_view()
        self.create_export_view()

    def valid_company_and_get_next_project(self, event):
        """
        验证日期及公司的选项是否符合规矩。
        并且，获取符合要求的项目内容。
        :param event: FocusOut
        :return:
        """
        if event.widget == self.company_combo:
            company_choose_data = self.company_combo.get_values().split(',')
            time_choose_data = self.date_combo.get_values().split(',')
            if "全选" in time_choose_data:
                time_choose_data.remove("全选")
            if "全选" in company_choose_data:
                company_choose_data.remove("全选")
            if time_choose_data == [""] or company_choose_data == [""]:
                showerror(title="选项错误", message="日期及公司不能为空")
            else:
                data = self.dynamic.get_project_items(company=company_choose_data, date=time_choose_data)
                self.project_combo.config_self(values=data)
                self.project_combo.hide_picker()

    def get_next_company(self, event):
        """
        根据日期设置符合要求的公司选项。
        :param event: FocusOut & FocusIn
        :return:
        """
        if event.widget == self.date_combo or event.widget == self.company_combo:
            self.company_list.clear()
            time_choose_data = self.date_combo.get_values().split(',')
            if "全选" in time_choose_data:
                time_choose_data.remove("全选")
            for company in self.data_resource.company_sheet_detail.keys():
                for company_date in self.data_resource.company_sheet_detail[company].keys():
                    if company_date[-4:] in time_choose_data:
                        self.company_list.append(BasicMessage.get_full_by_abb(company))
            self.company_list = list(set(self.company_list))
            self.company_list.insert(0, "全选")
            self.company_combo.config_self(values=self.company_list)

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

        self.date_combo = Combopicker(self.choose_frame, values=self.dynamic.time_choose())
        self.date_combo.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.date_combo.bind("<FocusOut>", self.get_next_company)

        company_label = tkinter.Label(self.choose_frame, text="请选择公司：（必选）", justify="left", anchor="w", padx=2)
        company_label.grid(row=1, column=0, sticky=tkinter.NSEW)

        _data = list(BasicMessage.company_abbreviation.keys())
        _data.insert(0, "全选")
        self.company_combo = Combopicker(self.choose_frame, values=_data)
        self.company_combo.bind("<FocusIn>", self.get_next_company)
        self.company_combo.bind("<FocusOut>", self.valid_company_and_get_next_project)
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

        query_button = ttk.Button(self.choose_frame, text="查询", command=self.export_excel)
        query_button.grid(row=5, column=1)

    def choose_cost(self):
        """
        覆盖现有视图，弹出新界面供选择
        :return:
        """
        choose_page_basic_frame = tkinter.Frame(self.root,
                                                width=1920,
                                                height=1080,
                                                )
        choose_page_basic_frame.grid_rowconfigure(0, weight=1, minsize=choose_page_basic_frame.winfo_reqheight()/20)
        choose_page_basic_frame.grid_rowconfigure(1, weight=18, minsize=choose_page_basic_frame.winfo_reqheight()*17/20)
        choose_page_basic_frame.grid_rowconfigure(2, weight=1, minsize=choose_page_basic_frame.winfo_reqheight()/20)
        choose_page_basic_frame.grid_rowconfigure(3, weight=1, minsize=choose_page_basic_frame.winfo_reqheight()/20)
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

        button_frame = tkinter.Frame(choose_page_basic_frame)
        button_frame.grid(row=2, column=2)

        sure_button = ttk.Button(button_frame, text="确认", command=choose_page_basic_frame.destroy, width=20,)
        sure_button.grid(row=0, column=1)

        cancel_button = ttk.Button(button_frame, text="返回", command=choose_page_basic_frame.destroy, width=20, )
        cancel_button.grid(row=0, column=0)

        choose_page_basic_frame.place(relx=0, rely=0)

    def pri(self):
        print(self.date_combo.get())
        print(self.company_combo.get())

    def create_tree_view(self):
        """
        构建表格，没有数据
        :return:
        """
        tableColumns = ['公司', '项目', '费用类别', '部门', '当月金额', '当年累计', '当月同比', '当月环比', "当年同比"]
        # 设置滚动条
        x_scroll = tkinter.Scrollbar(self.tree_frame, orient=tkinter.HORIZONTAL)
        y_scroll = tkinter.Scrollbar(self.tree_frame, orient=tkinter.VERTICAL)
        x_scroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        y_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.table = ttk.Treeview(
            master=self.tree_frame,  # 父容器
            columns=tableColumns,  # 列标识符列表
            height=50,  # 表格显示的行数
            show='headings',  # 隐藏首列
            style='Treeview',  # 样式
            xscrollcommand=x_scroll.set,  # x轴滚动条
            yscrollcommand=y_scroll.set  # y轴滚动条
        )
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        self.table.pack()  # TreeView加入frame
        # ['公司', '项目', '费用类别', '部门', '当月金额', '当年累积', '当月同比', '当月环比', '当年同比']
        self.table.heading(column=0, text="公司", anchor=tkinter.CENTER)
        self.table.column("公司", width=150, anchor=tkinter.CENTER)

        self.table.heading(column=1, text="项目", anchor=tkinter.CENTER)
        self.table.column("项目", width=150, anchor=tkinter.CENTER)

        self.table.heading(column=2, text="费用类别", anchor=tkinter.CENTER)
        self.table.column("费用类别", width=150, anchor=tkinter.CENTER)

        self.table.heading(column=3, text="部门", anchor=tkinter.CENTER)
        self.table.column("部门", width=150, anchor=tkinter.CENTER)

        self.table.heading(column=4, text="当月金额", anchor=tkinter.CENTER)
        self.table.column("当月金额", width=100, anchor=tkinter.CENTER)

        self.table.heading(column=5, text="当年累计", anchor=tkinter.CENTER)
        self.table.column("当年累计", width=100, anchor=tkinter.CENTER)

        self.table.heading(column=6, text="当月同比", anchor=tkinter.CENTER)
        self.table.column("当月同比", width=100, anchor=tkinter.CENTER)

        self.table.heading(column=7, text="当月环比", anchor=tkinter.CENTER)
        self.table.column("当月环比", width=100, anchor=tkinter.CENTER)

        self.table.heading(column=8, text="当年同比", anchor=tkinter.CENTER)
        self.table.column("当年同比", width=100, anchor=tkinter.CENTER)

    def create_export_view(self):
        export_button = ttk.Button(self.export_frame, text="导出为Excel", command=self.export_excel)
        export_button.place(relx=0.1, rely=0.8)

    def export_excel(self):
        pass
