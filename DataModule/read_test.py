import BasicMessage
import pandas as pd
import time


class FirstDeal:
    def __init__(self, filepath):
        self.file_path = filepath
        self.company_sheet_name_dict = {}
        self.company_abb = list(BasicMessage.company_abbreviation.values())
        self.company_all = list(BasicMessage.company_abbreviation.keys())

        # 尝试打开文件，得到sheet_name
        try:
            self.workbook_sheets_names = pd.read_excel(self.file_path, sheet_name=None).keys()
        except:
            print("somethings wrong")

        self.deal_sheets()
        self.deal_department(sheet_page=self.company_sheet_name_dict["之了成都教育"]["之了成都教育2206"])

    def deal_sheets(self):
        """
        处理文件相关sheets name 数据规整
        company_sheet_name_dict  :  各公司简写名字的对应有的表名
        :return: None
        """
        for x in self.company_abb:
            if x not in self.company_sheet_name_dict:
                self.company_sheet_name_dict[x] = {}
            else:
                pass

        for item_company_abb in self.company_abb:
            for item_sheet_name in self.workbook_sheets_names:
                if item_company_abb in item_sheet_name:
                    sheet_data = pd.read_excel(self.file_path, sheet_name=item_sheet_name)
                    self.company_sheet_name_dict[item_company_abb][item_sheet_name] = sheet_data if not sheet_data.empty else None

    # self.company_sheet_name_dict[item_company_abb][item_sheet_name]
    def deal_department(self, sheet_page):
        a = sheet_page.to_list()
        print(a)






if __name__ == '__main__':
    a = FirstDeal("/Users/MikeImac/Desktop/FinaceTool/经营检测表（费用明细表）数据底稿.xlsx")

