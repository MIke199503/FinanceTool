#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool
@File    ：BasicMessage.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/8 10:47 AM
"""

#  公司缩写
company_abbreviation = {"成都环宇知了科技有限公司": "环宇",
                        "成都标学科技有限公司": "标学",
                        "成都智慧树商贸有限公司": "智慧树",
                        "成都汇千科技有限公司": "汇千",
                        "成都之了会计职业技能培训学校": "之了学校",
                        "成都多人行科技有限公司": "多人行",
                        "之了（成都）科技有限公司": "之了成都",
                        "之了（云南）教育科技有限公司": "之了云南",
                        "北京之了科技有限公司": "北京之了",
                        "之了（北京）教育科技有限公司": "之了北京",
                        "逗学（山西）教育科技有限公司": "逗学山西",
                        "成都分王科技有限公司": "成都分王",
                        "之了（成都）教育科技有限公司": "之了成教",
                        "之了（成都）教育科技有限公司锦江区分公司": "之了锦江",
                        "之了（北京）教育科技有限公司太原分公司": "之了太原",
                        "之了课堂（成都）科技有限公司": "之了课堂",
                        }

template_data = {v: k for k, v in company_abbreviation.items()}
# item_data = [com,
#              "",
#              index,
#              "",
#              0,
#              "",
#              "",
#              "",
#              "",
#              ]
# item_data = [com,
#              "",
#              teme,
#              "",
#              self.data.company_sheet_detail[com][com_time]["Level1"]["total"][teme][0],
#              self.data.company_sheet_detail[com][com_time]["Level1"]["total"][teme][1],
#              self.get_total_circle(date=self.date[0], company=com, level="Level1",
#                                    keys=teme)[0],
#              self.get_total_circle(date=self.date[0], company=com, level="Level1",
#                                    keys=teme)[
#                  1],
#              self.get_total_circle(date=self.date[0], company=com, level="Level1",
#                                    keys=teme)[
#                  2],
#              ]
def get_full_by_abb(abb):
    return template_data[abb]

# 字典样式
# data = {"公式简称1": {
#                     "公司+日期1": {
#                                     "Leval1": {"code": [], "data": [
#                                     ["科目代码","部门","项目","本期借方发生","本期借方累积"]
#                                     ]},
#                                     "Leval2": {"code": [], "data": []},
#                                     "Leval3": {"code": [], "data": []},
#                                     "Leval4": {"code": [], "data": []},
#                                     "Leval5": {"code": [], "data": []},
#                                  },
#                     "公司+日期2": {
#                                     "Leval1": {"code": [], "data": []},
#                                     "Leval2": {"code": [], "data": []},
#                                     "Leval3": {"code": [], "data": []},
#                                     "Leval4": {"code": [], "data": []},
#                                     "Leval5": {"code": [], "data": []},
#                                 }
#                     },
#
#         "公式简称2": {
#                     "公司+日期1": {
#                                     "Leval1": {"code": [], "data": []},
#                                     "Leval2": {"code": [], "data": []},
#                                     "Leval3": {"code": [], "data": []},
#                                     "Leval4": {"code": [], "data": []},
#                                     "Leval5": {"code": [], "data": []},
#                                  },
#                     "公司+日期2": {
#                                     "Leval1": {"code": [], "data": []},
#                                     "Leval2": {"code": [], "data": []},
#                                     "Leval3": {"code": [], "data": []},
#                                     "Leval4": {"code": [], "data": []},
#                                     "Leval5": {"code": [], "data": []},
#                                 }
#                     }
# }

