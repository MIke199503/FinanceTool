#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool
@File    ：QueryClass.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/8 10:52 AM 
"""

import ReadExcel


class Query_Module:
    def __init__(self, data):
        self.data = data

    def query(self, date, company, project, cost_categories, depart):
        return_data_module = ["公司", "项目", "费用类别", "部门", "当月金额", " 当年累积"]


if __name__ == '__main__':
    a = ReadExcel.FirstDeal("/Users/MikeImac/Desktop/FinanceTool/经营检测表（费用明细表）数据底稿.xlsx")
    aa = a.company_sheet_detail
    qu = Query_Module(data=aa)
    # result = qu.query(date="2206", company="", project="", cost_categories="", depart="")
    # print(result)
