from tkinter import *

root = Tk()

my_var = StringVar()


# defining the callback function (observer)
def my_callback(var, index, mode):
    print("Traced variable {}".format(my_var.get()))


# registering the observer
my_var.trace_add('write', my_callback)

Label(root, textvariable=my_var).pack(padx=5, pady=5)

Entry(root, textvariable=my_var).pack(padx=5, pady=5)

root.mainloop()
