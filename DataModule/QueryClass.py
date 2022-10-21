#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool
@File    ：QueryClass.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/8 10:52 AM 
"""
from DataModule.ReadExcel import FirstDeal
import random
from DataModule.BasicMessage import company_abbreviation
from tkinter.messagebox import showerror


class Query_Module:
    def __init__(self, data: FirstDeal, date, company, project, cost_categories, depart):
        self.data = data
        self.date = date
        self.company = []
        for x in company:
            self.company.append(company_abbreviation[x])
        self.project = project
        self.cost = cost_categories
        self.depart = depart
        self.mode = "单日期"
        self.date_mode_choose()
        self.return_data = []
        _data_template = [["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]]
        self.only_time_company()

    def date_mode_choose(self):
        if len(self.date) == 1:
            self.mode = "单日期"
        else:
            self.mode = "多日期"

    def only_time_company(self):
        """
        处理日期+公司
        :return:
        """
        # [["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]]
        if self.mode == "单日期":
            for com in self.company:
                com_time = com+self.date[0]
                try:
                    sheets_data = self.data.company_sheet_detail[com][com_time]["Level1"]["total"].keys()
                except:
                    showerror(titel="发生错误", message="无法获取对应数据，请重新选择，或联系：朱桃禾")
                else:
                    for teme in sheets_data:
                        item_data = [com,
                                     "",
                                     teme,
                                     "",
                                     self.data.company_sheet_detail[com][com_time]["Level1"]["total"][teme][0],
                                     self.data.company_sheet_detail[com][com_time]["Level1"]["total"][teme][1],
                                     self.get_total_circle(date=self.date[0], company=com,level="Level1", keys=teme)[0],
                                     self.get_total_circle(date=self.date[0], company=com, level="Level1", keys=teme)[
                                         1],
                                     self.get_total_circle(date=self.date[0], company=com, level="Level1", keys=teme)[
                                         2],
                                     ]
                        self.return_data.append(item_data)
        else:
            for com in self.company:
                for time in self.date:
                    com_time = com + time
                    if com_time in self.data.company_sheet_detail[com].keys():
                        if self.data.company_sheet_detail[com][com_time]["Level1"]["total"] != {}:
                            for index in self.data.company_sheet_detail[com][com_time]["Level1"]["total"].keys():
                                self.add_value(com, index, self.data.company_sheet_detail[com][com_time]["Level1"]["total"][index][0])
                    else:
                        continue
            print(self.return_data)

    def time_company_project(self):
            pass

    def add_value(self, company, cost_index, data):
        """
        多日期的添加模式
        :param company:
        :param cost_index:
        :param data: 需要添加的数据
        :return:
        """
        print("当前数据:",self.return_data)
        if self.return_data == []:
            self.return_data.append([company, "", cost_index, "", float(data), "", "", "", "",])
        else:
            flag = 0
            for item in self.return_data:
                if item[0] == company and item[2] == cost_index:
                    index = self.return_data.index(item)
                    self.return_data[index][4] += float(data)
                    flag = 1
            if flag == 0:
                self.return_data.append([company, "", cost_index, "", float(data), "", "", "", "", ])
        print("操作后的数据:", self.return_data)

        print("*"*10)



    def get_total_circle(self, date, company, level, keys):
        """
        获取对应科目下的总体数据的同，环，年同
        :param date:
        :param company:
        :param level:
        :param keys:
        :return: 同，环 ，年同
        """
        # 同比直接计算
        tongbi = company + str(int(date) - 100)

        # 计算时间边缘
        if date[-2:] == "01":
            circle_bi = company + str(int(date[0:2]) - 1) + str(12)
        else:
            circle_bi = company + str(int(date) - 1)

        # 当月金额
        basic_yue = self.data.company_sheet_detail[company][company + date][level]["total"][keys][0]
        # 当年累计
        basic_year = self.data.company_sheet_detail[company][company + date][level]["total"][keys][1]

        if tongbi in self.data.company_sheet_detail[company].keys():
            # 同比-当月 数据
            tong_num = self.data.company_sheet_detail[company][tongbi][level]["total"][keys][0]
            # 同比-当年 数据
            tong_year_num = self.data.company_sheet_detail[company][tongbi][level]["total"][keys][1]

        else:
            tong_num = None
            tong_year_num = None

        if circle_bi in self.data.company_sheet_detail[company].keys():
            # 环比-当月 数据
            circle_num = self.data.company_sheet_detail[company][circle_bi][level]["total"][keys][0]
        else:
            circle_num = None

        # 月同
        if tong_num is None or float(tong_num) == 0.0:
            year_tong_data = "0"
        else:
            year_tong_data = "{:.2f}%".format(((float(basic_yue) - float(tong_num)) / float(tong_num)) * 100)

        # 月环
        if circle_num is None or float(circle_num) == 0.0:
            circle_data = "0"
        else:
            circle_data = "{:.2f}%".format(((float(basic_yue) - float(circle_num)) / float(circle_num)) * 100)

        # 年同
        if tong_year_num is None or float(tong_year_num) == 0.0:
            tong_year_total = "0"
        else:
            tong_year_total = "{:.2f}%".format(((float(basic_year) - float(tong_year_num)) / float(tong_year_num)) * 100)
        # print("keys:", keys)
        # print("当月金额:", basic_yue)
        # print("当年累计:", basic_year)
        # print("当月同比数据:", tong_num)
        # print("当年同比数据:", tong_year_num)
        # print("当月环比数据:", circle_num)
        # print(year_tong_data, circle_data, tong_year_total)
        return year_tong_data, circle_data, tong_year_total

    def query(self):
        return self.return_data


