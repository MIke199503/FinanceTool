# from tkinter import ttk
# import tkinter as tk
#
# root = tk.Tk()
# tree1 = ttk.Treeview(root, columns=("公司", "数字"), show="tree headings")
#
# tree1.heading(column=0, text="公司", anchor=tk.CENTER)
# tree1.column("公司", width=150, anchor=tk.CENTER)
#
# tree1.heading(column=1, text="数字", anchor=tk.CENTER)
# tree1.column("数字", width=150, anchor=tk.CENTER)
#
# tree1.pack()
#
# numlist = [["6601.01","123"],["6601.01.01","-3344"]]
# tree1.tag_configure("red", foreground="red")
# tree1.tag_configure("green", foreground="green")
# # 参数:parent, index, id=None, **kw (父节点，排序，id不能相同，显示出的文本)
# subtree1 = tree1.insert("", 0, id="1", values=numlist[0])  # ""表示父节点是根
# tree1.insert(subtree1, 0, id="101", values=numlist[1], tags="red" if int(numlist[1][1]) < 0 else "green")  # text表示显示出的文本，values是隐藏的值
# tree1.insert(subtree1, 1, id="102", values=numlist[0], tags="red" if int(numlist[0][1]) < 0 else "green")
# root.mainloop()
#
# # self.tree = ttk.Treeview(parent, columns=("size", "modified"))
# # self.tree["columns"] = ("date", "time", "loc")
# #
# # self.tree.column("#0", width=100, anchor='center')
# # self.tree.column("date", width=100, anchor='center')
# # self.tree.column("time", width=100, anchor='center')
# # self.tree.column("loc", width=100, anchor='center')
# #
# # self.tree.heading("#0", text="Name")
# # self.tree.heading("date", text="Date")
# # self.tree.heading("time", text="Time")
# # self.tree.heading("loc", text="Location")
# #
# # self.tree.insert("", "end", text="Grace",
# #                  values=("2010-09-23", "03:44:53", "Garden"))
# # self.tree.insert("", "end", text="John",
# #                  values=("2017-02-05", "11:30:23", "Airport"))
# # self.tree.insert("", "end", text="Betty",
# #                  values=("2014-06-25", "18:00:00", ""))


import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title('Theme Demo')
        self.geometry('400x300')
        self.style = ttk.Style(self)

        # label
        label = ttk.Label(self, text='Name:')
        label.grid(column=0, row=0, padx=10, pady=10,  sticky='w')
        # entry
        textbox = ttk.Entry(self)
        textbox.grid(column=1, row=0, padx=10, pady=10,  sticky='w')
        # button
        btn = ttk.Button(self, text='Show')
        btn.grid(column=2, row=0, padx=10, pady=10,  sticky='w')

        # radio button
        self.selected_theme = tk.StringVar()
        theme_frame = ttk.LabelFrame(self, text='Themes')
        theme_frame.grid(padx=10, pady=10, ipadx=20, ipady=20, sticky='w')

        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(
                theme_frame,
                text=theme_name,
                value=theme_name,
                variable=self.selected_theme,
                command=self.change_theme)
            rb.pack(expand=True, fill='both')

    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()
