#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool
@File    ：QueryClass.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/8 10:52 AM 
"""
from DataModule.ReadExcel import FirstDeal
from DataModule.BasicMessage import company_abbreviation
from DataModule.BasicMessage import get_full_by_abb
from tkinter.messagebox import showerror
from DataModule.GetDynamicData import Dynamic_Data


# ['']
# ['']
# ['']
# [[], [], [], []]
# ['']

class Query_Module:
    def __init__(self, data: FirstDeal, date, company, project, cost_categories, depart):
        self.data = data
        self.date = date
        self.company = []
        for x in company:
            self.company.append(company_abbreviation[x])
        self.project = project

        self.cost = cost_categories[:]
        self.cost.reverse()

        self.depart = depart
        self.mode = "单日期"
        self.date_mode_choose()
        self.return_data = []
        _data_template = [["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当月同", "当月环", "当年同"]]
        self.level_list = ["Level1", "Level2", "Level3", "Level4", "Level5"]
        self.dynamic = Dynamic_Data(data_resource=self.data)

    def date_mode_choose(self):
        """
        处理日期模式
        :return:
        """
        if len(self.date) == 1:
            self.mode = "单日期"
        else:
            self.mode = "多日期"

    def time_company_project_cost_depart(self):
        if self.mode == "单日期":
            for com in self.company:
                basic = self.deal_single_page_tcpcd(com=com, time=self.date[0])
                time_data = self.get_compare_time(com=com, time=self.date[0])
                tong_bi_time = time_data[0][-4:]
                circle_bi_time = time_data[1][-4:]
                tong_bi_data = self.deal_single_page_tcpcd(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tcpcd(com=com, time=circle_bi_time)
                for detail_data in basic:
                    basic_yue = detail_data[4]
                    basic_year = detail_data[5]
                    tong_yue = None
                    tong_year = None
                    circle_yue = None
                    # 获取对应的目标月同，年同数据
                    flag = 0
                    for tong in tong_bi_data:
                        if tong[0] == detail_data[0] and tong[1] == detail_data[1] and tong[2] == detail_data[2] and \
                                tong[3] == detail_data[3]:
                            tong_yue = tong[4]
                            tong_year = tong[5]
                            flag = 1
                    if flag == 0:
                        tong_year = None
                        tong_yue = None
                    # 获取对应的目标月环
                    flag1 = 0
                    for circle in circle_bi_data:
                        if circle[0] == detail_data[0] and circle[1] == detail_data[1] and circle[2] == detail_data[
                            2] and circle[3] == detail_data[3]:
                            circle_yue = circle[4]
                            flag1 = 1
                    if flag1 == 0:
                        circle_yue = None

                    # 月同
                    if tong_yue is None or float(tong_yue) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(((float(basic_yue) - float(tong_yue)) / float(tong_yue)) * 100)

                    # 月环
                    if circle_yue is None or float(circle_yue) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(circle_yue)) / float(circle_yue)) * 100)

                    # 年同
                    if tong_year is None or float(tong_year) == 0.0:
                        tong_year_total = "0"
                    else:
                        tong_year_total = "{:.2f}%".format(
                            ((float(basic_year) - float(tong_year)) / float(tong_year)) * 100)

                    index = basic.index(detail_data)
                    basic[index][6] = yue_tong_data
                    basic[index][7] = circle_data
                    basic[index][8] = tong_year_total
                for item in basic:
                    self.return_data.append(item)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcpcd(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[6] = ""
                    index[7] = ""
                    index[5] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] \
                                    and self.return_data[target][1] == index[1] \
                                    and self.return_data[target][2] == index[2] \
                                    and self.return_data[target][3] == index[3]:
                                self.return_data[target][4] += index[4]
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def time_company_cost_depart(self):
        if self.mode == "单日期":
            for com in self.company:
                basic = self.deal_single_page_tccd(com=com, time=self.date[0])
                tong_bi_time = self.get_compare_time(com=com, time=self.date[0])[0][-4:]
                circle_bi_time = self.get_compare_time(com=com, time=self.date[0])[1][-4:]
                tong_bi_data = self.deal_single_page_tccd(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tccd(com=com, time=circle_bi_time)
                for item_detail in basic:
                    basic_yue = item_detail[4]
                    basic_year = item_detail[5]
                    tong_yue_target = None
                    tong_year_target = None
                    circle_target = None
                    for tong in tong_bi_data:
                        if tong[0] == item_detail[0] and tong[2] == item_detail[2] and tong[3] == item_detail[3]:
                            tong_yue_target = tong[4]
                            tong_year_target = tong[5]
                    for circle in circle_bi_data:
                        if circle[0] == item_detail[0] and circle[2] == item_detail[2] and circle[3] == item_detail[3]:
                            circle_target = circle[4]
                    # 月同

                    if tong_yue_target is None or float(tong_yue_target) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(tong_yue_target)) / float(tong_yue_target)) * 100)

                    # 月环
                    if circle_target is None or float(circle_target) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(circle_target)) / float(circle_target)) * 100)

                    # 年同
                    if tong_year_target is None or float(tong_year_target) == 0.0:
                        tong_year_data = "0"
                    else:
                        tong_year_data = "{:.2f}%".format(
                            ((float(basic_year) - float(tong_year_target)) / float(tong_year_target)) * 100)
                    index = basic.index(item_detail)
                    basic[index][6] = yue_tong_data
                    basic[index][7] = circle_data
                    basic[index][8] = tong_year_data
                    self.return_data.append(item_detail)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tccd(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[5] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][2] == index[2] and \
                                    self.return_data[target][3] == index[3]:
                                self.return_data[target][4] += index[4]
                                self.return_data[target][5] = ""
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def time_company_project_depart(self):
        """
        处理搜索逻辑：日期+公司+项目+部门
        :return:
        """
        if self.mode == "单日期":
            for com in self.company:
                basic = self.deal_single_page_tcpd(com=com, time=self.date[0])
                tong_bi_time = self.get_compare_time(com=com, time=self.date[0])[0][-4:]
                circle_bi_time = self.get_compare_time(com=com, time=self.date[0])[1][-4:]
                tong_bi_data = self.deal_single_page_tcpd(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tcp(com=com, time=circle_bi_time)
                for item_detail in basic:
                    basic_yue = item_detail[4]
                    basic_year = item_detail[5]
                    tong_yue_target = None
                    tong_year_target = None
                    circle_target = None
                    for tong in tong_bi_data:
                        if tong[0] == item_detail[0] and tong[1] == item_detail[1] and tong[2] == item_detail[2]:
                            tong_yue_target = tong[4]
                            tong_year_target = tong[5]
                    for circle in circle_bi_data:
                        if circle[0] == item_detail[0] and circle[1] == item_detail[1] and circle[2] == item_detail[2]:
                            circle_target = circle[4]
                    # 月同

                    if tong_yue_target is None or float(tong_yue_target) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(tong_yue_target)) / float(tong_yue_target)) * 100)

                    # 月环
                    if circle_target is None or float(circle_target) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(circle_target)) / float(circle_target)) * 100)

                    # 年同
                    if tong_year_target is None or float(tong_year_target) == 0.0:
                        tong_year_data = "0"
                    else:
                        tong_year_data = "{:.2f}%".format(
                            ((float(basic_year) - float(tong_year_target)) / float(tong_year_target)) * 100)

                    index = basic.index(item_detail)

                    basic[index][6] = yue_tong_data
                    basic[index][7] = circle_data
                    basic[index][8] = tong_year_data
                    self.return_data.append(item_detail)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcpd(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[5] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][2] == index[2] and \
                                    self.return_data[target][1] == index[1]:
                                self.return_data[target][4] += index[4]
                                self.return_data[target][5] = ""
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def time_company_project_cost(self):
        """
        处理搜索逻辑：日期+公司+项目+费用类别
        :return:
        """
        if self.mode == "单日期":
            for com in self.company:
                basic = self.deal_single_page_tcpc(com=com, time=self.date[0])
                tong_bi_time = self.get_compare_time(com=com, time=self.date[0])[0][-4:]
                circle_bi_time = self.get_compare_time(com=com, time=self.date[0])[1][-4:]
                tong_bi_data = self.deal_single_page_tcpc(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tcpc(com=com, time=circle_bi_time)
                for item_detail in basic:
                    basic_yue = item_detail[4]
                    basic_year = item_detail[5]
                    tong_yue_target = None
                    tong_year_target = None
                    circle_target = None
                    for tong in tong_bi_data:
                        if tong[0] == item_detail[0] and tong[1] == item_detail[1] and tong[2] == item_detail[2]:
                            tong_yue_target = tong[4]
                            tong_year_target = tong[5]
                    for circle in circle_bi_data:
                        if circle[0] == item_detail[0] and circle[1] == item_detail[1] and circle[2] == item_detail[2]:
                            circle_target = circle[4]
                    # 月同

                    if tong_yue_target is None or float(tong_yue_target) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(tong_yue_target)) / float(tong_yue_target)) * 100)

                    # 月环
                    if circle_target is None or float(circle_target) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(circle_target)) / float(circle_target)) * 100)

                    # 年同
                    if tong_year_target is None or float(tong_year_target) == 0.0:
                        tong_year_data = "0"
                    else:
                        tong_year_data = "{:.2f}%".format(
                            ((float(basic_year) - float(tong_year_target)) / float(tong_year_target)) * 100)

                    index = basic.index(item_detail)
                    basic[index][6] = yue_tong_data
                    basic[index][7] = circle_data
                    basic[index][8] = tong_year_data
                    self.return_data.append(item_detail)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcpc(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[5] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][2] == index[2] and \
                                    self.return_data[target][1] == index[1]:
                                self.return_data[target][4] += index[4]
                                self.return_data[target][5] = ""
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def time_company_depart(self):
        """
        处理搜索逻辑：日期+公司+部门。
        :return:
        """
        if self.mode == "单日期":
            for com in self.company:
                # [[],[]]
                basic_data = self.deal_single_page_tcd(com=com, time=self.date[0])
                tong_bi_time = self.get_compare_time(com=com, time=self.date[0])[0][-4:]
                circle_bi_time = self.get_compare_time(com=com, time=self.date[0])[1][-4:]
                tong_bi_data = self.deal_single_page_tcd(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tcd(com=com, time=circle_bi_time)
                for item_detail in basic_data:
                    basic = item_detail[4]
                    tong_target = None
                    circle_target = None
                    for tong in tong_bi_data:
                        if tong[0] == item_detail[0] and tong[3] == item_detail[3]:
                            tong_target = tong[4]
                    for circle in circle_bi_data:
                        if circle[0] == item_detail[0] and circle[3] == item_detail[3]:
                            circle_target = circle[4]
                    # 月同

                    if tong_target is None or float(tong_target) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(
                            ((float(basic) - float(tong_target)) / float(tong_target)) * 100)

                    # 月环
                    if circle_target is None or float(circle_target) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic) - float(circle_target)) / float(circle_target)) * 100)

                    index = basic_data.index(item_detail)
                    basic_data[index][6] = yue_tong_data
                    basic_data[index][7] = circle_data
                    self.return_data.append(item_detail)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcd(com=com, time=time))
            for item in com_list:
                for index in item:
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][3] == index[3]:
                                self.return_data[target][4] += index[4]
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def time_company_cost(self):
        """
        处理搜索逻辑：日期+公司+费用类别
        :return:
        """
        if self.mode == "单日期":
            for com in self.company:
                basic_data = self.deal_single_page_tcc(com=com, time=self.date[0])
                time_data = self.get_compare_time(com=com, time=self.date[0])
                tong_bi_time = time_data[0][-4:]
                circle_bi_time = time_data[1][-4:]
                tong_bi_data = self.deal_single_page_tcc(com=com, time=tong_bi_time)
                circle_bi_data = self.deal_single_page_tcc(com=com, time=circle_bi_time)
                for detail_data in basic_data:
                    basic_yue = detail_data[4]
                    basic_year = detail_data[5]
                    tong_yue = None
                    tong_year = None
                    circle_yue = None
                    # 获取对应的目标月同，年同数据
                    flag = 0
                    for tong in tong_bi_data:
                        if tong[0] == detail_data[0] and tong[2] == detail_data[2]:
                            tong_yue = tong[4]
                            tong_year = tong[5]
                            flag = 1
                    if flag == 0:
                        tong_year = None
                        tong_yue = None
                    # 获取对应的目标月环
                    flag1 = 0
                    for circle in circle_bi_data:
                        if circle[0] == detail_data[0] and circle[2] == detail_data[2]:
                            circle_yue = circle[4]
                            flag1 = 1
                    if flag1 == 0:
                        circle_yue = None

                    # 月同
                    if tong_yue is None or float(tong_yue) == 0.0:
                        yue_tong_data = "0"
                    else:
                        yue_tong_data = "{:.2f}%".format(((float(basic_yue) - float(tong_yue)) / float(tong_yue)) * 100)

                    # 月环
                    if circle_yue is None or float(circle_yue) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_yue) - float(circle_yue)) / float(circle_yue)) * 100)

                    # 年同
                    if tong_year is None or float(tong_year) == 0.0:
                        tong_year_total = "0"
                    else:
                        tong_year_total = "{:.2f}%".format(
                            ((float(basic_year) - float(tong_year)) / float(tong_year)) * 100)

                    index = basic_data.index(detail_data)
                    basic_data[index][6] = yue_tong_data
                    basic_data[index][7] = circle_data
                    basic_data[index][8] = tong_year_total
                for item in basic_data:
                    self.return_data.append(item)
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcc(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[6] = ""
                    index[7] = ""
                    index[5] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][2] == index[2]:
                                self.return_data[target][4] += index[4]
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def only_time_company(self):
        """
        处理日期+公司
        :return:
        """
        # [["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]]
        if self.mode == "单日期":
            for com in self.company:
                com_time = com + self.date[0]
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
                                     self.get_total_circle(date=self.date[0], company=com, level="Level1", keys=teme)[
                                         0],
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
                                self.add_value_basic_mode(com, index,
                                                          self.data.company_sheet_detail[com][com_time]["Level1"][
                                                              "total"][index][
                                                              0])
                    else:
                        continue

    def time_company_project(self):
        """
        处理搜索逻辑：日期+公司+项目
        :return:
        """
        if self.mode == "单日期":
            for com in self.company:
                data = self.deal_single_page_tcp(com=com, time=self.date[0])
                tong_bi = self.get_compare_time(com=com, time=self.date[0])[0]
                circle_bi = self.get_compare_time(com=com, time=self.date[0])[1]
                tong_compare_data = self.deal_single_page_tcp(com=com, time=tong_bi[-4:])
                circle_compare_data = self.deal_single_page_tcp(com=com, time=circle_bi[-4:])
                for x in range(len(data)):
                    basic_num = data[x][4]
                    tong_bi_num = 0
                    circle_bi_num = 0
                    for item in tong_compare_data:
                        if data[x][0] == item[0] and data[x][1] == item[1]:
                            tong_bi_num = item[4]
                    for index in circle_compare_data:
                        if data[x][0] == index[0] and data[x][1] == index[1]:
                            circle_bi_num = index[4]

                    if tong_bi_num is None or float(tong_bi_num) == 0.0:
                        tong_data = "0"
                    else:
                        tong_data = "{:.2f}%".format(
                            ((float(basic_num) - float(tong_bi_num)) / float(tong_bi_num)) * 100)

                    if circle_bi_num is None or float(circle_bi_num) == 0.0:
                        circle_data = "0"
                    else:
                        circle_data = "{:.2f}%".format(
                            ((float(basic_num) - float(circle_bi_num)) / float(circle_bi_num)) * 100)
                    data[x][6] = tong_data
                    data[x][7] = circle_data
                    self.return_data.append(data[x])
        else:
            com_list = []  # [[[]],[[],[]]
            self.return_data.clear()
            for com in self.company:
                for time in self.date:
                    com_list.append(self.deal_single_page_tcp(com=com, time=time))
            for item in com_list:
                for index in item:
                    index[6] = ""
                    index[7] = ""
                    if not self.return_data:
                        self.return_data.append(index)
                    else:
                        flag = 0
                        for target in range(len(self.return_data)):
                            if self.return_data[target][0] == index[0] and self.return_data[target][1] == index[1]:
                                self.return_data[target][4] += index[4]
                                flag = 1
                        if flag == 0:
                            self.return_data.append(index)

    def get_compare_time(self, com, time):
        """
        获取对应的同环比时间周期，包含公司名字
        :param com:
        :param time: "2206"
        :return: 同比时间，环比时间
        """
        tong_bi = com + str(int(time) - 100)
        # 计算时间边缘
        if time[-2:] == "01":
            circle_bi = com + str(int(time[0:2]) - 1) + str(12)
        else:
            circle_bi = com + str(int(time) - 1)
        return tong_bi, circle_bi

    def deal_single_page_tcp(self, com, time):
        """
        用于：日期+时间+项目逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return: 【【】，【】】
        """
        page_return_data = []
        com_time = com + time
        if com_time in self.data.company_sheet_detail[com].keys():
            for level in self.level_list:
                for tem_data in self.data.company_sheet_detail[com][com_time][level]["data"]:
                    if tem_data[2] in self.project:
                        # ["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]
                        # ["公司", "项目", "", "", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]
                        if not page_return_data:
                            page_return_data.append([com, tem_data[2], "", "", float(tem_data[3]), "", 0, 0, ""])
                        else:
                            flag = 0
                            for item in page_return_data:
                                if item[0] == com and item[1] == tem_data[2]:
                                    index = page_return_data.index(item)
                                    page_return_data[index][4] += float(tem_data[3])
                                    flag = 1
                            if flag == 0:
                                page_return_data.append(
                                    [com, tem_data[2], "", "", float(tem_data[3]), "", 0, 0, ""])
        return page_return_data

    def deal_single_page_tcc(self, com, time):
        """
        用于：日期+时间+费用类别逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        cost_useful = self.cost.copy()
        if com_time in self.data.company_sheet_detail[com].keys():
            for cost_index in range(len(cost_useful)):
                index_true = 4 - cost_index
                if not cost_useful[cost_index]:
                    continue
                else:
                    try:
                        sheets_data = self.data.company_sheet_detail[com][com_time]["Level" + str(index_true)][
                            "total"].keys()
                    except:
                        showerror(titel="发生错误", message="无法获取对应数据，请重新选择，或联系：朱桃禾")
                    else:
                        for tem_data in sheets_data:
                            if tem_data in cost_useful[cost_index]:
                                if not page_return:
                                    page_return.append([com,
                                                        "",
                                                        tem_data,
                                                        "",
                                                        self.data.company_sheet_detail[com][com_time][
                                                            "Level" + str(index_true)]["total"][tem_data][0],
                                                        self.data.company_sheet_detail[com][com_time][
                                                            "Level" + str(index_true)]["total"][tem_data][1],
                                                        "",
                                                        "",
                                                        ""])
                                else:
                                    flag = 0
                                    for item in page_return:
                                        if item[0] == com and item[2] == tem_data:
                                            index = page_return.index(item)
                                            page_return[index][4] += float(
                                                self.data.company_sheet_detail[com][com_time][
                                                    "Level" + str(index_true)]["total"][tem_data][0])
                                            page_return[index][5] += float(
                                                self.data.company_sheet_detail[com][com_time][
                                                    "Level" + str(index_true)]["total"][tem_data][1])
                                            flag = 1
                                    if flag == 0:
                                        page_return.append([com,
                                                            "",
                                                            tem_data,
                                                            "",
                                                            self.data.company_sheet_detail[com][com_time][
                                                                "Level" + str(index_true)]["total"][tem_data][0],
                                                            self.data.company_sheet_detail[com][com_time][
                                                                "Level" + str(index_true)]["total"][tem_data][1],
                                                            "",
                                                            "",
                                                            ""])
                    break
        return page_return

    def deal_single_page_tcd(self, com, time):
        """
        用于：日期+时间+部门逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        if com_time in self.data.company_sheet_detail[com].keys():
            for level in self.level_list:
                try:
                    sheets_data = self.data.company_sheet_detail[com][com_time][level]["data"]
                except:
                    showerror(titel="发生错误", message="无法获取对应数据，请重新选择，或联系：朱桃禾")
                else:
                    for tem_data in sheets_data:
                        if tem_data[1] in self.depart:
                            if not page_return:
                                page_return.append([com,
                                                    "",
                                                    "",
                                                    tem_data[1],
                                                    tem_data[3],
                                                    "",
                                                    "",
                                                    "",
                                                    ""])
                            else:
                                flag = 0
                                for item in page_return:
                                    if item[0] == com and item[3] == tem_data[1]:
                                        index = page_return.index(item)
                                        page_return[index][4] += float(tem_data[3])
                                        flag = 1
                                if flag == 0:
                                    page_return.append([com,
                                                        "",
                                                        "",
                                                        tem_data[1],
                                                        tem_data[3],
                                                        "",
                                                        "",
                                                        "",
                                                        ""])
        return page_return

    def deal_single_page_tcpc(self, com, time):
        """
        用于：日期+时间+项目+费用类别逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        cost_useful = self.cost.copy()
        if com_time in self.data.company_sheet_detail[com].keys():
            for cost_index in range(len(cost_useful)):
                if not cost_useful[cost_index]:
                    continue
                else:
                    for project in self.project:
                        for cost_item in cost_useful[cost_index]:
                            item_new = self.get_total_cost_project(com=com, date=time, project=project,
                                                                   cost=cost_item)
                            if item_new is not None:
                                page_return.append(item_new)
                    break
        return page_return

    def deal_single_page_tcpd(self, com, time):
        """
        用于：日期+时间+项目+部门类别逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        if com_time in self.data.company_sheet_detail[com].keys():
            for level in self.level_list:
                for item in self.data.company_sheet_detail[com][com_time][level]["data"]:
                    if item[1] in self.depart and item[2] in self.project:
                        if not page_return:
                            page_return.append([com, item[2], "", item[1], item[3], item[4], "", "", ""])
                        else:
                            flag = 0
                            for index in page_return:
                                if index[0] == com and index[1] == item[2] and index[3] == item[1]:
                                    i = page_return.index(index)
                                    page_return[i][4] += item[3]
                                    page_return[i][5] += item[4]
                                    flag = 1
                            if flag == 0:
                                page_return.append([com, item[2], "", item[1], item[3], item[4], "", "", ""])
        return page_return

    def deal_single_page_tccd(self, com, time):
        """
        用于：日期+时间+费用类别+部门逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        cost_useful = self.cost.copy()
        if com_time in self.data.company_sheet_detail[com].keys():
            for cost_index in range(len(cost_useful)):
                index_true = 4 - cost_index
                level = "Level" + str(index_true)
                if not cost_useful[cost_index]:
                    continue
                else:
                    for cost_item in cost_useful[cost_index]:
                        for depart in self.depart:
                            item_new = self.get_total_cost_depart(com=com, date=time, depart=depart, cost=cost_item)
                            if item_new is not None:
                                page_return.append(item_new)
                    break
        return page_return

    def deal_single_page_tcpcd(self, com, time):
        """
        用于：日期+时间+项目+费用类别+部门逻辑时处理单张sheet表的数据
        :param com:
        :param time:
        :return:
        """
        page_return = []
        com_time = com + time
        cost_useful = self.cost.copy()
        useful_cost_index = 3
        for x in cost_useful:
            if not x:
                continue
            else:
                useful_cost_index = cost_useful.index(x)
                break
        if com_time in self.data.company_sheet_detail[com].keys():
            for project in self.project:
                for cost in cost_useful[useful_cost_index]:
                    for depart in self.depart:
                        if self.check_project_depart(com=com, date=time, level="Level" + str(4 - useful_cost_index),
                                                     project=project, depart=depart):
                            item_new = self.get_total_cost_project_depart(com=com, date=time, depart=depart, cost=cost,
                                                                          project=project)
                            if item_new is not None:
                                page_return.append(item_new)
                        else:
                            continue
        return page_return

    def check_project_depart(self, com, date, level, project, depart):
        """
        检验对应等级下，是否存在该部门和项目。
        :param com:
        :param date:
        :param level:
        :param project:
        :param depart:
        :return:
        """
        flag = 0
        level1 = level
        while int(level1[-1:]) <= 5:
            for item in self.data.company_sheet_detail[com][com + date][level1]["data"]:
                if item[1] == depart and item[2] == project:
                    flag = 1
                    break
            level1 = "Level" + str(int(level1[-1:]) + 1)

        if flag == 1:
            return True
        else:
            return False

    def get_total_cost_project_depart(self, com, date, project, cost, depart):
        """
        获取项目费用类别的纵深总和
        :param depart:
        :param com:
        :param date:
        :param project:
        :param cost:
        :return:
        """
        level_index = None
        com_time = com + date
        code = cost.split("-")[0]
        data_item = [com, project, cost, depart, 0, 0, "", "", ""]
        if len(code) == 4:
            level_index = "Level1"
        elif len(code) == 7:
            level_index = "Level2"
        elif len(code) == 10:
            level_index = "Level3"
        elif len(code) == 13:
            level_index = "Level4"
        elif len(code) == 16:
            level_index = "Level5"
        if level_index is not None:
            for item in self.data.company_sheet_detail[com][com_time][level_index]["data"]:
                if item[0] == code and item[2] == project and item[1] == depart:
                    data_item[4] += float(item[3])
                    data_item[5] += float(item[4])
            while int(level_index[-1:]) <= 4:
                level_index = level_index[:-1] + str(int(level_index[-1:]) + 1)
                for it in self.data.company_sheet_detail[com][com_time][level_index]["data"]:
                    if code in it[0] and it[2] == project and it[1] == depart:
                        data_item[4] += float(it[3])
                        data_item[5] += float(it[4])
            if data_item == [com, project, cost, depart, 0, 0, "", "", ""]:
                return None
            else:
                return data_item
        else:
            return None

    def get_total_cost_depart(self, com, date, depart, cost):
        """
        获取项目费用类别的纵深总和---组合依据：部门
        :param depart:
        :param com:
        :param date:
        :param cost:
        :return:
        """
        level_index = None
        com_time = com + date
        code = cost.split("-")[0]
        data_item = [com, "", cost, depart, 0, 0, "", "", ""]
        if len(code) == 4:
            level_index = "Level1"
        elif len(code) == 7:
            level_index = "Level2"
        elif len(code) == 10:
            level_index = "Level3"
        elif len(code) == 13:
            level_index = "Level4"
        elif len(code) == 16:
            level_index = "Level5"

        if level_index is not None:
            for item in self.data.company_sheet_detail[com][com_time][level_index]["data"]:
                if item[0] == code and item[1] == depart:
                    data_item[4] += float(item[3])
                    data_item[5] += float(item[4])
            while int(level_index[-1:]) <= 4:
                level_index = level_index[:-1] + str(int(level_index[-1:]) + 1)
                for it in self.data.company_sheet_detail[com][com_time][level_index]["data"]:
                    if code in it[0] and it[1] == depart:
                        data_item[4] += float(it[3])
                        data_item[5] += float(it[4])
            if data_item == [com, "", cost, depart, 0, 0, "", "", ""]:
                return None
            else:
                return data_item
        else:
            return None

    def get_total_cost_project(self, com, date, project, cost):
        """
        获取项目费用类别的纵深总和
        :param com:
        :param date:
        :param project:
        :param cost:
        :return:
        """
        level_index = None
        com_time = com + date
        code = cost.split("-")[0]
        data_item = [com, project, cost, "", 0, 0, "", "", ""]

        if len(code) == 4:
            level_index = "Level1"
        elif len(code) == 7:
            level_index = "Level2"
        elif len(code) == 10:
            level_index = "Level3"
        elif len(code) == 13:
            level_index = "Level4"
        elif len(code) == 16:
            level_index = "Level5"

        if level_index is None:
            return None
        else:
            while int(level_index[-1:]) <= 5:
                for it in self.data.company_sheet_detail[com][com_time][level_index]["data"]:
                    if (code in it[0] or code == it[0]) and it[2] == project:
                        data_item[4] += float(it[3])
                        data_item[5] += float(it[4])
                level_index = level_index[:-1] + str(int(level_index[-1:]) + 1)
            if data_item == [com, project, cost, "", 0, 0, "", "", ""]:
                return None
            else:
                return data_item

    def add_value_basic_mode(self, company, cost_index, data):
        """
        多日期的添加模式
        :param company:
        :param cost_index:
        :param data: 需要添加的数据
        :return:
        """
        if not self.return_data:
            self.return_data.append([company, "", cost_index, "", float(data), "", "", "", "", ])
        else:
            flag = 0
            for item in self.return_data:
                if item[0] == company and item[2] == cost_index:
                    index = self.return_data.index(item)
                    self.return_data[index][4] += float(data)
                    flag = 1
            if flag == 0:
                self.return_data.append([company, "", cost_index, "", float(data), "", "", "", "", ])

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
        tongbi = self.get_compare_time(com=company, time=date)[0]
        circle_bi = self.get_compare_time(com=company, time=date)[1]
        # 当月金额
        basic_yue = self.data.company_sheet_detail[company][company + date][level]["total"][keys][0]
        # 当年累计
        basic_year = self.data.company_sheet_detail[company][company + date][level]["total"][keys][1]

        if tongbi in self.data.company_sheet_detail[company].keys():
            # 同比-当月 数据
            # 同比-当年 数据
            if keys in self.data.company_sheet_detail[company][tongbi][level]["total"].keys():
                tong_num = self.data.company_sheet_detail[company][tongbi][level]["total"][keys][0]
                tong_year_num = self.data.company_sheet_detail[company][tongbi][level]["total"][keys][1]
            else:
                tong_num = None
                tong_year_num = None
        else:
            tong_num = None
            tong_year_num = None

        if circle_bi in self.data.company_sheet_detail[company].keys():
            # 环比-当月 数据
            if keys in self.data.company_sheet_detail[company][circle_bi][level]["total"].keys():
                circle_num = self.data.company_sheet_detail[company][circle_bi][level]["total"][keys][0]
            else:
                circle_num = None
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
            tong_year_total = "{:.2f}%".format(
                ((float(basic_year) - float(tong_year_num)) / float(tong_year_num)) * 100)
        return year_tong_data, circle_data, tong_year_total

    def query(self):
        self.return_data.clear()
        if self.project == [''] and self.cost == [[], [], [], []] and self.depart == ['']:
            self.only_time_company()
            print("tc")
        elif self.project != [''] and self.cost == [[], [], [], []] and self.depart == ['']:
            self.time_company_project()
            print("tcp")
        elif self.project == [''] and self.cost != [[], [], [], []] and self.depart == ['']:
            self.time_company_cost()
            print("tcc")
        elif self.project == [''] and self.cost == [[], [], [], []] and self.depart != ['']:
            self.time_company_depart()
            print("tcd")
        elif self.project != [''] and self.cost != [[], [], [], []] and self.depart == ['']:
            self.time_company_project_cost()
            print("tcpc")
        elif self.project != [''] and self.cost == [[], [], [], []] and self.depart != ['']:
            self.time_company_project_depart()
            print("tcpd")
        elif self.project == [''] and self.cost != [[], [], [], []] and self.depart != ['']:
            self.time_company_cost_depart()
            print("tccd")
        elif self.project != [''] and self.cost != [[], [], [], []] and self.depart != ['']:
            self.time_company_project_cost_depart()
            print("tcpcd")
        else:
            showerror(title="查询错误", message="未知查询逻辑！请联系研发人员！！")
        return self.return_data
