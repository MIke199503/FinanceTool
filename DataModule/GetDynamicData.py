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
        self.cost_category_return_data = {"Level1": set(),
                                          "Level2": set(),
                                          "Level3": set(),
                                          "Level4": set(),
                                          "Level5": set(),
                                          }
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
                    complete_index = company_index + date_index
                    if complete_index in self.resource.company_sheet_detail[company_index].keys():
                        template_data = self.resource.company_sheet_detail[company_index][complete_index]
                        for level_index in self.level_list:
                            for item in template_data[level_index]["data"]:
                                if not item:
                                    pass
                                else:
                                    project_items.add(item[2])
            project_items = list(project_items)
            project_items.sort()
            project_items.insert(0, "全选")
            return project_items
        return []

    def deal_code_deep(self, company, date, data):
        """
        根据给定的数据，将其纵深相关的费用类别都添加进去
        :param company: 具体的公司简称
        :param date: 公司简称+时间
        :param data: 数据行
        :return: None
        """
        code = data[0]
        if len(code) >= 16:
            for x in self.resource.company_sheet_detail[company][date]["Level5"]["code"]:
                if code in x:
                    self.cost_category_return_data["Level5"].add(x)
        if len(code) > 13:
            for x in self.resource.company_sheet_detail[company][date]["Level4"]["code"]:
                if code[:13] in x:
                    self.cost_category_return_data["Level4"].add(x)
        if len(code) == 13:
            for x in self.resource.company_sheet_detail[company][date]["Level4"]["code"]:
                if code[:] in x:
                    self.cost_category_return_data["Level4"].add(x)
        if len(code) >= 10:
            for x in self.resource.company_sheet_detail[company][date]["Level3"]["code"]:
                if code[:10] in x:
                    self.cost_category_return_data["Level3"].add(x)
        if len(code) == 10:
            for x in self.resource.company_sheet_detail[company][date]["Level3"]["code"]:
                if code[:] in x:
                    self.cost_category_return_data["Level3"].add(x)
        if len(code) > 7:
            for x in self.resource.company_sheet_detail[company][date]["Level2"]["code"]:
                if code[:7] in x:
                    self.cost_category_return_data["Level2"].add(x)
        if len(code) == 7:
            for x in self.resource.company_sheet_detail[company][date]["Level2"]["code"]:
                if code[:] in x:
                    self.cost_category_return_data["Level2"].add(x)
        if len(code) > 4:
            for x in self.resource.company_sheet_detail[company][date]["Level1"]["code"]:
                if code[:4] in x:
                    self.cost_category_return_data["Level1"].add(x)
        if len(code) == 4:
            for x in self.resource.company_sheet_detail[company][date]["Level1"]["code"]:
                if code[:] in x:
                    self.cost_category_return_data["Level1"].add(x)

    def get_cost_category(self, company, date, project):
        """
        获取所有的费用类别列表
        :param company: list /【""】
        :param date: list /【""】
        :param project: list /【""】
        :return:self.cost_category_return_data= {"Level1": set(),
                                          "Level2": set(),
                                          "Level3": set(),
                                          "Level4": set(),
                                          "Level5": set(),
                                          }
        """
        self.cost_category_return_data = {"Level1": set(),
                                          "Level2": set(),
                                          "Level3": set(),
                                          "Level4": set(),
                                          "Level5": set(),
                                          }
        for x in company:
            company_abb = company_abbreviation[x]
            com_date = list(self.resource.company_sheet_detail[company_abb].keys())
            for time in date:
                if company_abb + time in com_date:
                    for level_index in self.level_list:
                        if project == [""]:
                            code_keys = list(
                                self.resource.company_sheet_detail[company_abb][company_abb + time][level_index][
                                    "code"])
                            for code_key in code_keys:
                                self.cost_category_return_data[level_index].add(code_key)
                        else:
                            detail_data_list = \
                                self.resource.company_sheet_detail[company_abb][company_abb + time][level_index]['data']
                            for item in detail_data_list:
                                if item[2] in project:
                                    self.deal_code_deep(company=company_abb, date=company_abb + time, data=item)
        sort_data = self.cost_category_return_data.copy()

        for x in sort_data.keys():
            list_convert = list(sort_data[x])
            list_convert.sort()
            sort_data[x] = list_convert
        return sort_data

    def get_depart_category(self, date_choose_list, company_choose_list, project_choose_list, cost_choose_list):
        """
        根据选择信息，获取对应的部门提示信息，
        若全选、空选、仅选一级科目，返回所有，若单选选择对应层级的部门信息
        :param date_choose_list: list
        :param company_choose_list: list
        :param project_choose_list: list
        :param cost_choose_list: list
        :return: depart部门信息列表
        """
        date_choose_list = date_choose_list
        company_choose_list = company_choose_list
        project_choose_list = project_choose_list
        cost_choose_list = cost_choose_list
        cost_choose_list.reverse()
        depart = set()

        # 有效的日期
        useful_company = []
        for date in date_choose_list:
            for company in company_choose_list:
                com_abb = company_abbreviation[company]
                com_date = com_abb + date
                if com_date in self.resource.company_sheet_detail[com_abb]:
                    useful_company.append(com_date)
        # 判断筛选逻辑
        mode = 0
        if cost_choose_list[0] == [] and cost_choose_list[1] == [] and \
                cost_choose_list[2] == [] and cost_choose_list[3] == []:
            mode = 0
        elif cost_choose_list[1] == [] and cost_choose_list[1] == [] and \
                cost_choose_list[2] == [] and cost_choose_list[3] != []:
            mode = 0
        else:
            mode = 1

        # 获取数据
        for use_item in useful_company:
            company_data = self.resource.company_sheet_detail[use_item[:-4]][use_item]
            if mode == 0:
                for level in self.level_list:
                    for tem in company_data[level]["data"]:
                        if project_choose_list != [""]:
                            if tem[2] in project_choose_list:
                                depart.add(tem[1])
                        else:
                            depart.add(tem[1])
            elif mode == 1:
                for index, item in enumerate(cost_choose_list):
                    item_data = []
                    if item:
                        for x in item:
                            item_data.append(x.split('-')[0])
                        level_message = "Level" + str(4 - index)
                        for tem_data in company_data[level_message]["data"]:
                            if project_choose_list != [""]:
                                if tem_data[2] in project_choose_list and tem_data[0] in item_data:
                                    depart.add(tem_data[1])
                            else:
                                if tem_data[0] in item_data:
                                    depart.add(tem_data[1])
                        break
                    else:
                        continue

        return depart
