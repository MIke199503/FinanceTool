import openpyxl
import BasicMessage
import pandas as pd
from openpyxl.utils import get_column_letter
import GetDepartment

class FirstDeal:
    def __init__(self, filepath):
        self.file_path = filepath
        self.company_sheet_name_dict = {}

        # 尝试打开文件，得到wb
        try:
            self.wb = openpyxl.load_workbook(filepath)
            self.workbook_sheets_names = self.wb.sheetnames
            self.return_data = self.read_single_sheet_table("之了成都教育2206")
            testa = GetDepartment.GetDepart(self.return_data)
            testa.get_one_leval()
        except:
            print("somethings wrong")

        self.deal_sheets()

    def deal_sheets(self):
        """
        处理文件相关sheets name 数据规整
        company_sheet_name_dict  :  各公司简写名字的对应有的表名
        :return: None
        """
        company_abb = list(BasicMessage.company_abbreviation.values())
        # company_all = list(BasicMessage.company_abbreviation.keys())

        for x in company_abb:
            if x not in self.company_sheet_name_dict:
                self.company_sheet_name_dict[x] = {}
            else:
                pass

        for item_company_abb in company_abb:
            for item_sheet_name in self.workbook_sheets_names:
                if item_company_abb in item_sheet_name:
                    sheet_data = pd.read_excel(self.file_path, sheet_name=item_sheet_name)
                    self.company_sheet_name_dict[item_company_abb][item_sheet_name] = sheet_data

        print(self.company_sheet_name_dict)

    def read_single_sheet_table(self, sheet_name):
        ws = self.wb[sheet_name]
        max_row_num = ws.max_row
        max_col_num = ws.max_column
        data = []
        for row in range(2, max_row_num+1):
            row_item = []
            for col in range(1, max_col_num):
                col_letter = get_column_letter(col)
                row_item.append(ws[col_letter+str(row)].value)
            data.append(row_item)
        return data


if __name__ == '__main__':
    a = FirstDeal("/Users/zhutaohe/Desktop/FInanceTool/经营检测表（费用明细表）数据底稿.xlsx")
