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

class Query_Module:
    def __init__(self, data: FirstDeal, date, company, project, cost_categories, depart):
        self.data = data
        self.date = date
        self.company = company
        self.project = project
        self.cost = cost_categories
        self.depart = depart
        self.mode = self.mode_deal()

    def mode_deal(self):
        mode = 0
        if self.project == [] and self.cost == [[], [], []] and self.depart == []:
            mode = 1

        return mode

    def query(self):
        return_data_module = [["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积", "当年同", "当年环", "当年同"]]
        a = self.data.company_sheet_detail["之了成教"]["之了成教2206"]["Level3"]["data"]
        b = self.data.company_sheet_detail["之了成教"]["之了成教2205"]["Level2"]["data"]
        c = random.choice([a, b])
        return c


