#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool
@File    ：QueryClass.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/8 10:52 AM 
"""


class Query_Module:
    def __init__(self, data, date, company, project, cost_categories, depart):
        self.data = data
        self.date = date
        self.company = company
        self.project = project
        self.cost = cost_categories
        self.depart = depart
        self.mode = self.mode_deal()

    def mode_deal(self):
        return 1

    def query(self):
        # return_data_module = ["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积","当年同","当年环","当年同"]
        pass


