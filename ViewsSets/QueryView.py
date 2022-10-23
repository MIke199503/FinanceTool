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
import openpyxl
from ViewsSets.ComBoPicker import Combopicker
from DataModule import BasicMessage
from DataModule.GetDynamicData import Dynamic_Data
from ViewsSets.CheckList import CheckBox
from DataModule.QueryClass import Query_Module
from tkinter.filedialog import asksaveasfilename


class QueryView:
    def __init__(self, root_page, data_resource=None):
        """
        三分布局，三个Frame，打底
        :param root_page:父级视图
        """

        self.depart_choose_data = None
        self.choose_page_basic_frame = None
        self.leval_1_picker = None
        self.leval_2_picker = None
        self.leval_3_picker = None
        self.leval_4_picker = None

        self.cost_result = tkinter.StringVar()

        self.cost_data = None
        self.data_resource = data_resource

        self.dynamic = Dynamic_Data(data_resource=self.data_resource)

        self.table = None
        self.project_combo = None
        self.company_combo = None
        self.date_combo = None
        self.depart_combo = None

        self.time_choose_data = []  # 选择的时间信息
        self.company_choose_data = []  # 选择的公司信息
        self.project_choose_data = []  # 选择的项目信息
        self.cost_choose_data = [[], [], [], []]  # 选择的费用类别
        self.depart_choose_data = []  # 选择的部门信息

        self.root = root_page  # 父级视图

        # 加个底
        self.basic_frame = ttk.Frame(self.root, width=1920, height=900)
        self.basic_frame.grid_rowconfigure(0, weight=1, minsize=self.basic_frame.winfo_reqheight())
        # self.basic_frame.grid_rowconfigure(1, weight=1, minsize=self.basic_frame.winfo_reqheight() / 20)
        self.basic_frame.grid_columnconfigure(0, weight=3, minsize=self.basic_frame.winfo_reqwidth() * 3 / 14)
        self.basic_frame.grid_columnconfigure(1, weight=11, minsize=self.basic_frame.winfo_reqwidth() * 9 / 14)
        self.basic_frame.grid_columnconfigure(2, weight=1)
        self.basic_frame.place(relx=0, rely=0)

        # 选项视图
        self.choose_frame = ttk.Frame(self.basic_frame, )
        self.choose_frame["padding"] = (5, 5, 5, 5)
        self.choose_frame.grid_columnconfigure(0, weight=1, )
        self.choose_frame.grid_columnconfigure(1, weight=2, )
        self.choose_frame.grid(row=0, column=0, sticky=tkinter.NSEW)

        # 表格视图
        self.tree_frame = ttk.PanedWindow(self.basic_frame)
        self.tree_frame.grid(row=0, column=1, sticky=tkinter.NSEW)

        # 导出视图
        self.export_frame = ttk.Frame(self.basic_frame)
        self.export_frame.grid(row=0, column=2, sticky=tkinter.NSEW)

        # 构建详细界面
        self.create_choose_item()
        self.create_tree_view()
        self.create_export_view()

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
        time_label = ttk.Label(self.choose_frame, text="请选择日期：（必选）", justify="left", anchor="w")
        time_label.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.date_combo = Combopicker(self.choose_frame, values=self.dynamic.time_choose())
        self.date_combo.grid(row=0, column=1, sticky=tkinter.NSEW, pady=7)
        self.date_combo.bind("<FocusOut>", self.get_next_company)

        company_label = ttk.Label(self.choose_frame, text="请选择公司：（必选）", justify="left", anchor="w")
        company_label.grid(row=1, column=0, sticky=tkinter.NSEW)

        _data = list(BasicMessage.company_abbreviation.keys())
        _data.insert(0, "全选")
        self.company_combo = Combopicker(self.choose_frame, values=_data)
        self.company_combo.bind("<FocusIn>", self.get_next_company)
        self.company_combo.bind("<FocusOut>", self.valid_company_and_get_next_project)
        self.company_combo.grid(row=1, column=1, sticky=tkinter.NSEW, pady=7)

        project_label = ttk.Label(self.choose_frame, text="请选择项目：", justify="left", anchor="w")
        project_label.grid(row=2, column=0, sticky=tkinter.NSEW)

        self.project_combo = Combopicker(self.choose_frame, values=[""])
        self.project_combo.bind("<FocusIn>", self.valid_company_and_get_next_project)
        self.project_combo.grid(row=2, column=1, sticky=tkinter.NSEW, pady=7)

        cost_label = ttk.Label(self.choose_frame, text="请选择费用类别：", justify="left", anchor="w")
        cost_label.grid(row=3, column=0, sticky=tkinter.NSEW)

        cost_result = ttk.Entry(self.choose_frame, textvariable=self.cost_result, width=30, state="normal")
        cost_result.grid(row=3, column=1, sticky=tkinter.NSEW, pady=7)

        cost_button = ttk.Button(self.choose_frame, text="点击进入选择页面", command=self.choose_cost)
        cost_button.grid(row=4, column=1, sticky=tkinter.NSEW, pady=7)

        depart_label = ttk.Label(self.choose_frame, text="请选择部门：", justify="left", anchor="w")
        depart_label.grid(row=5, column=0, sticky=tkinter.NSEW)

        self.depart_combo = Combopicker(self.choose_frame, values=["全选"])
        self.depart_combo.grid(row=5, column=1, sticky=tkinter.NSEW, pady=7)

        query_button = ttk.Button(self.choose_frame, text="查询", command=self.start_query, width=20)
        query_button.grid(row=6, column=1, pady=7)

    def choose_cost(self):
        """
        覆盖现有视图，弹出新界面供选择
        :return:
        """
        self.get_cost_category_data()
        self.choose_page_basic_frame = ttk.Frame(self.root,
                                                 width=1920,
                                                 height=800,
                                                 )
        self.choose_page_basic_frame.grid_rowconfigure(0, weight=1,
                                                       minsize=self.choose_page_basic_frame.winfo_reqheight() / 20)
        self.choose_page_basic_frame.grid_rowconfigure(1, weight=18,
                                                       minsize=self.choose_page_basic_frame.winfo_reqheight() * 17 / 20)
        self.choose_page_basic_frame.grid_rowconfigure(2, weight=1,
                                                       minsize=self.choose_page_basic_frame.winfo_reqheight() / 20)
        self.choose_page_basic_frame.grid_rowconfigure(3, weight=1,
                                                       minsize=self.choose_page_basic_frame.winfo_reqheight() / 20)
        self.choose_page_basic_frame.grid_columnconfigure(0, weight=1,
                                                          minsize=self.choose_page_basic_frame.winfo_reqwidth() / 4)
        self.choose_page_basic_frame.grid_columnconfigure(1, weight=1,
                                                          minsize=self.choose_page_basic_frame.winfo_reqwidth() / 4)
        self.choose_page_basic_frame.grid_columnconfigure(2, weight=1,
                                                          minsize=self.choose_page_basic_frame.winfo_reqwidth() / 4)
        self.choose_page_basic_frame.grid_columnconfigure(3, weight=1,
                                                          minsize=self.choose_page_basic_frame.winfo_reqwidth() / 4)

        leval_1_label = ttk.Label(self.choose_page_basic_frame, text="请选择一级标题",
                                  anchor="w",
                                  justify="left")
        leval_1_label.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.leval_1_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level1"],
                                       command=self.get_next_level2_data)
        self.leval_1_picker.grid(row=1, column=0, sticky=tkinter.NSEW)

        leval_2_label = ttk.Label(self.choose_page_basic_frame, text="请选择二级科目",
                                  anchor="w",
                                  justify="left")
        leval_2_label.grid(row=0, column=1, sticky=tkinter.NSEW)

        self.leval_2_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level2"])
        self.leval_2_picker.grid(row=1, column=1, sticky=tkinter.NSEW)

        leval_3_label = ttk.Label(self.choose_page_basic_frame, text="请选择三级科目",
                                  anchor="w",
                                  justify="left")
        leval_3_label.grid(row=0, column=2, sticky=tkinter.NSEW)

        self.leval_3_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level3"])
        self.leval_3_picker.grid(row=1, column=2, sticky=tkinter.NSEW)

        leval_4_label = ttk.Label(self.choose_page_basic_frame, text="请选择四级科目",
                                  anchor="w",
                                  justify="left")
        leval_4_label.grid(row=0, column=3, sticky=tkinter.NSEW)

        self.leval_4_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level4"])
        self.leval_4_picker.grid(row=1, column=3, sticky=tkinter.NSEW)

        button_frame = ttk.Frame(self.choose_page_basic_frame)
        button_frame.grid(row=2, column=3)

        sure_button = ttk.Button(button_frame, text="确认", command=self.click_cost_button, width=20, )
        sure_button.grid(row=0, column=1)

        cancel_button = ttk.Button(button_frame, text="返回", command=self.cancel_cost_choose_page, width=20, )
        cancel_button.grid(row=0, column=0)

        self.choose_page_basic_frame.place(relx=0, rely=0)

    def create_tree_view(self):
        """
        构建表格，没有数据
        :return:
        """
        tableColumns = ['公司', '项目', '费用类别', '部门', '当月金额', '当年累计', '当月同比', '当月环比',
                        "当年同比"]
        # 设置滚动条
        y_scroll = ttk.Scrollbar(self.tree_frame, orient=tkinter.VERTICAL)
        s = ttk.Style()
        s.configure("Treeview", rowheight=40)
        s.configure("Treeview.Heading",
                    font=(None, 15, "bold"),
                    # rowheight=int(15*1),
                    # foreground="white"
                    )

        self.table = ttk.Treeview(
            master=self.tree_frame,  # 父容器
            columns=tableColumns,  # 列标识符列表
            height=20,  # 表格显示的行数
            show='headings',  # 隐藏首列
            style='Treeview',  # 样式
            yscrollcommand=y_scroll.set,  # y轴滚动条
        )
        y_scroll.grid(row=0, column=1, sticky=tkinter.NSEW)
        y_scroll.config(command=self.table.yview)
        self.table.grid(row=0, column=0)  # TreeView加入frame
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
        """
        创建导出Excel按钮
        :return:
        """
        export_button = ttk.Button(self.export_frame, text="导出为Excel", command=self.export_excel)
        export_button.pack(side=tkinter.LEFT, pady=15, padx=15, anchor=tkinter.SW)

    def get_next_company(self, event):
        """
        根据日期设置符合要求的公司选项。
        :param event: FocusOut & FocusIn
        :return:
        """
        if event.widget == self.date_combo or event.widget == self.company_combo:
            self.company_choose_data.clear()
            self.time_choose_data = self.date_combo.get_values().split(',')
            if self.time_choose_data == [""]:
                xa = list(BasicMessage.company_abbreviation.keys())
                self.company_choose_data = xa[:]
            if "全选" in self.time_choose_data:
                self.time_choose_data.remove("全选")
            for company in self.data_resource.company_sheet_detail.keys():
                for company_date in self.data_resource.company_sheet_detail[company].keys():
                    if company_date[-4:] in self.time_choose_data:
                        self.company_choose_data.append(BasicMessage.get_full_by_abb(company))
            self.company_choose_data = list(set(self.company_choose_data))
            if "成都环宇知了科技有限公司" in self.company_choose_data:
                self.company_choose_data.remove("成都环宇知了科技有限公司")
            self.company_choose_data.sort(reverse=True)
            self.company_choose_data.insert(0, "成都环宇知了科技有限公司")
            self.company_choose_data.insert(0, "全选")
            self.company_combo.config_self(values=self.company_choose_data)

    def valid_company_and_get_next_project(self, event):
        """
        验证日期及公司的选项是否符合规矩。
        并且，获取符合要求的项目内容。
        :param event: FocusOut
        :return:
        """
        self.company_choose_data = self.company_combo.get_values().split(',')
        self.time_choose_data = self.date_combo.get_values().split(',')
        if "全选" in self.time_choose_data:
            self.time_choose_data.remove("全选")
        if "全选" in self.company_choose_data:
            self.company_choose_data.remove("全选")
        if self.time_choose_data == [""] and self.company_choose_data == [""]:
            showerror(title="选项错误", message="日期及公司不能为空")
            if self.time_choose_data == [""]:
                self.date_combo.focus_set()
            if self.company_choose_data == [""]:
                self.company_combo.focus_set()
        else:
            data = self.dynamic.get_project_items(company=self.company_choose_data, date=self.time_choose_data)
            self.project_combo.config_self(values=data)
            self.project_combo.hide_picker()

    def get_cost_category_data(self):
        """
        获取费用类比选取所需的全部数据，后续的操作都是在这个基础上去更新
        :return:
        """
        self.project_choose_data = self.project_combo.get_values().split(',')
        self.company_choose_data = self.company_combo.get_values().split(',')
        self.time_choose_data = self.date_combo.get_values().split(',')
        if "全选" in self.time_choose_data:
            self.time_choose_data.remove("全选")
        if "全选" in self.company_choose_data:
            self.company_choose_data.remove("全选")
        if "全选" in self.project_choose_data:
            self.project_choose_data.remove("全选")
        if self.project_choose_data == [""] or self.company_choose_data == [""]:
            showerror(title="选项错误", message="日期及公司不能为空")
        else:
            self.cost_data = self.dynamic.get_cost_category(company=self.company_choose_data,
                                                            date=self.time_choose_data,
                                                            project=self.project_choose_data)
        return self.cost_data

    def get_next_level2_data(self):
        """
        根据一级费用类别的选择，获取二级费用类别的数据
        :return:
        """
        self.leval_2_picker.destroy()
        data = self.leval_1_picker.get_values()
        if "全选" in data:
            data.remove("全选")
        if not data:
            self.leval_2_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level2"][:],
                                           command=self.get_next_level3_data)
        else:
            new_data = []
            for x in data:
                for y in self.cost_data["Level2"]:
                    if x.split("-")[0] in y:
                        new_data.append(y)
            self.leval_2_picker = CheckBox(self.choose_page_basic_frame, values=new_data,
                                           command=self.get_next_level3_data)
        self.leval_2_picker.grid(row=1, column=1, sticky=tkinter.NSEW)

    def get_next_level3_data(self):
        """
        根据二级费用类别的选择，获取三级费用类别的数据
        :return:
        """
        self.leval_3_picker.destroy()
        data = self.leval_2_picker.get_values()
        if "全选" in data:
            data.remove("全选")
        if not data:
            self.leval_3_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level3"][:],
                                           command=self.get_next_level4_data)
        else:
            new_data = []
            for x in data:
                for y in self.cost_data["Level3"]:
                    if x.split("-")[0] in y:
                        new_data.append(y)
            self.leval_3_picker = CheckBox(self.choose_page_basic_frame, values=new_data,
                                           command=self.get_next_level4_data)
        self.leval_3_picker.grid(row=1, column=2, sticky=tkinter.NSEW)

    def get_next_level4_data(self):
        """
        根据三级费用类别的选择，获取四级费用类别的数据
        :return:
        """
        self.leval_4_picker.destroy()
        data = self.leval_3_picker.get_values()
        if "全选" in data:
            data.remove("全选")
        if not data:
            self.leval_4_picker = CheckBox(self.choose_page_basic_frame, values=self.cost_data["Level4"][:])
        else:
            new_data = []
            for x in data:
                for y in self.cost_data["Level4"]:
                    if x.split("-")[0] in y:
                        new_data.append(y)
            self.leval_4_picker = CheckBox(self.choose_page_basic_frame, values=new_data)
        self.leval_4_picker.grid(row=1, column=3, sticky=tkinter.NSEW)

    def click_cost_button(self):
        """
        获取费用类别的选项信息
        :return:
        """
        cost_level1_choose = self.leval_1_picker.get_values()
        cost_level2_choose = self.leval_2_picker.get_values()
        cost_level3_choose = self.leval_3_picker.get_values()
        cost_level4_choose = self.leval_4_picker.get_values()
        self.cost_choose_data.clear()
        self.cost_choose_data = [cost_level1_choose, cost_level2_choose, cost_level3_choose, cost_level4_choose]
        self.cost_result.set(str(self.cost_choose_data))
        data = list(self.dynamic.get_depart_category(date_choose_list=self.time_choose_data,
                                                     company_choose_list=self.company_choose_data,
                                                     project_choose_list=self.project_choose_data,
                                                     cost_choose_list=self.cost_choose_data))
        data.sort()
        data.insert(0, "全选")
        self.depart_combo.config_self(values=data)
        self.choose_page_basic_frame.destroy()

    def cancel_cost_choose_page(self):
        """
        选择费用类别页面的返回按钮回参
        :return:
        """
        self.choose_page_basic_frame.destroy()
        cost_level1_choose = []
        cost_level2_choose = []
        cost_level3_choose = []
        cost_level4_choose = []
        self.cost_choose_data.clear()
        self.cost_choose_data = [cost_level1_choose, cost_level2_choose, cost_level3_choose, cost_level4_choose]
        self.cost_result.set(str(self.cost_choose_data))

    def export_excel(self):
        """
        导出Excel文件
        :return:
        """
        local_data_index = self.table.get_children()
        if local_data_index != ():
            all_data = []
            for index in local_data_index:
                all_data.append(self.table.item(index)["values"])
            all_data.insert(0, ['公司', '项目', '费用类别', '部门', '当月金额', '当年累计', '当月同比', '当月环比',
                                "当年同比"])
            try:
                file_save_path = asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel file", ".xlsx")])
            except FileNotFoundError:
                showerror(title="未选择正确的文件", message="你没有选择、创建一个正确的Excel文件名")
            else:
                wb = openpyxl.Workbook()
                ws = wb.active
                for item in all_data:
                    ws.append(item)
                wb.save(file_save_path)
        else:
            showerror(title="暂无数据", message="表格中无有效数据，无法导出")

    def start_query(self):
        """
        查询按钮的回调函数
        加载对应的查询数据
        :return:
        """
        self.depart_choose_data = self.depart_combo.get_values().split(',')
        self.project_choose_data = self.project_combo.get_values().split(',')
        self.company_choose_data = self.company_combo.get_values().split(',')
        self.time_choose_data = self.date_combo.get_values().split(',')
        if "全选" in self.time_choose_data:
            self.time_choose_data.remove("全选")
        if "全选" in self.company_choose_data:
            self.company_choose_data.remove("全选")
        if "全选" in self.project_choose_data:
            self.project_choose_data.remove("全选")
        if "全选" in self.depart_choose_data:
            self.depart_choose_data.remove("全选")
        # print(self.time_choose_data)
        # print(self.company_choose_data)
        # print(self.project_choose_data)
        # print(self.cost_choose_data)
        # print(self.depart_choose_data)
        query_class = Query_Module(data=self.data_resource,
                                   date=self.time_choose_data,
                                   company=self.company_choose_data,
                                   project=self.project_choose_data,
                                   cost_categories=self.cost_choose_data,
                                   depart=self.depart_choose_data)
        return_data = query_class.query()
        obk = self.table.get_children()
        for item in obk:
            self.table.delete(item)
        for new_data in return_data:
            self.table.insert("", "end", values=new_data, open=True)
        del query_class
