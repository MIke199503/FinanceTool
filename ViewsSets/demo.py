#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：demo.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/9 10:11 AM 
"""

from tkinter import *
from ViewsSets.ComBoPicker import Combopicker  # 导入自定义下拉多选框

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x300")

    F = Frame(root)
    F.pack(expand=False, fill="both", padx=10, pady=10)
    Label(F, text='全选、可滚动：').pack(side='left')
    COMBOPICKER = Combopicker(F,
                              values=['全选', '项目1', '项目2', '项目3', '项目4', '项目5', '项目11', '项目22', '项目33', '项目44', '项目55'])
    COMBOPICKER.pack(anchor="w")

    root.mainloop()

