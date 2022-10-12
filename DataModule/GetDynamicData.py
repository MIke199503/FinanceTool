#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：GetDynamicData.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/12 9:06 AM 
"""
from DataModule.ReadExcel import FirstDeal
from DataModule.BasicMessage import company_abbreviation


class Dynamic_Data:
    """
    帮助获取一些动态数据
    """
    def __init__(self, data_resource: FirstDeal):
        """
        需要有基础表单数据
        :param data_resource:FirstDeal
        """
        self.resource = data_resource
        self.level_list = ["Level1", "Level2", "Level3", "Level4", "Level5"]

    def time_choose(self):
        """
        获取可用时间序列
        :return:
        """
        x = self.resource.get_time_data()
        x.insert(0, "全选")
        return x

    def get_project_items(self, company, date):
        """
        获取有效的project选项
        :param company: 公司名列表（全称）
        :param date: 日期
        :return:
        """
        project_items = set()
        company_abb_list = []
        if company != [""] and date != [""]:
            for x in company:
                company_abb_list.append(company_abbreviation[x])
            for company_index in company_abb_list:
                for date_index in date:
                    complete_index = company_index+date_index
                    if complete_index in self.resource.company_sheet_detail[company_index].keys():
                        template_data = self.resource.company_sheet_detail[company_index][complete_index]
                        for level_index in self.level_list:
                            for item in template_data[level_index]["data"]:
                                if not item:
                                    pass
                                else:
                                    project_items.add(item[2])
            project_items = list(project_items)
            project_items.insert(0, "全选")
            return project_items
        return []

