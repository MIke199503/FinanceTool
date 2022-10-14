#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FinanceTool 
@File    ：CheckList.py
@Author  ：朱桃禾 MikePy
@Date    ：2022/10/12 7:34 PM 
"""
from tkinter import *
from tkinter import ttk


class CheckBox(ttk.Frame):
    def __init__(self, master=None, active_background='#b1dcfb', width=200, height=900, values: list = [], active_foreground='black',
                 select_background='#003eff', select_foreground='white', command=None, border_width=2, relief="ridge"):
        #  flat, groove, raised, ridge, solid, or sunken
        super().__init__(master, borderwidth=border_width, relief=relief)
        self._selected_item = None

        self._values = values
        if not self._values:
            pass
        elif "全选" in self._values:
            self._values.remove("全选")
        self._values.insert(0, "全选")

        self._sel_bg = select_background
        self._sel_fg = select_foreground

        self._act_bg = active_background
        self._act_fg = active_foreground

        self._command = command
        self.index = 0

        Frame.__init__(self, master, borderwidth=border_width, width=width, height=height, relief=relief)

        F = Frame(self)
        F.pack(fill='x')
        self.canvas = Canvas(F, scrollregion=(0, 0, 500, (len(self._values) * 21)))

        vbar = Scrollbar(F, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.canvas.yview)

        frame = Frame(self.canvas)
        self.canvas.create_window((0, 0,), window=frame, anchor='nw', tags='frame')
        self.canvas.config(highlightthickness=0)  # 去掉选中边框
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=width, height=height)
        self.canvas.config(yscrollcommand=vbar.set)

        self.dict_checkbutton = []
        self.dict_checkbutton_var = {}
        self.item_flag = []
        for index, item in enumerate(self._values):
            var = StringVar()
            if item == "全选":
                var.trace_add("write", self.deal_choose_all)
            else:
                var.trace_add("write", self.data_change_callback)
            self.item_flag.append(var)
            self.check_item = Checkbutton(frame, text=item, variable=var, offvalue="", onvalue=item, anchor="w")
            self.dict_checkbutton.append(self.check_item)
            self.check_item.grid(row=index, column=0, sticky=NSEW, padx=5)

        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.canvas.bind("<MouseWheel>", self.processWheel)

        for i in self.dict_checkbutton:
            i.bind("<MouseWheel>", self.processWheel)

    def deal_choose_all(self, var, index, mode):
        tem = self.item_flag[0].get()
        if tem == "":
            for x in range(1, len(self.item_flag)):
                self.item_flag[x].set("")
        elif tem == "全选":
            for x in range(1, len(self.item_flag)):
                self.item_flag[x].set(self._values[x])
        self.data_change_callback(var, index, mode)

    def data_change_callback(self, var, index, mode):
        if self._command is None:
            print("123")
        else:
            self._command()

    def processWheel(self, event):
        a = int(-event.delta)
        if a > 0:
            self.canvas.yview_scroll(1, UNITS)
        else:
            self.canvas.yview_scroll(-1, UNITS)

    def get_values(self):
        value = []
        for item in range(len(self.item_flag)):
            if self.item_flag[item].get() == "全选":
                continue
            elif self.item_flag[item].get() != "":
                value.append(self.item_flag[item].get())
        return value


if __name__ == '__main__':
    root = Tk()
    choices = ["Author", "John", "Mohan", "James", "Ankur", "Robert"]
    def update_next():
        global c
        c.destroy()
        c = CheckBox(root, values=a.get_values())
        c.pack()

    a = CheckBox(root, values=choices, command=update_next)
    a.pack()

    c = CheckBox(root, values=[])
    c.pack()

    b = Button(root, text="Check", command=update_next)
    b.pack()

    root.mainloop()
