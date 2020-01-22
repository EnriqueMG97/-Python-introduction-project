from tkinter import *
from tkinter import ttk

from window import Window
from db_operations import DB_Operations

if __name__ == '__main__':
    window  = Tk()
    data = Window(window)
    db_op = DB_Operations(data.expenditure, data.price, data.message, data.tree)

    # Button to add an expense
    ttk.Button(data.frame, text = 'Save expense', command = db_op.add_expense).grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
    # Button to delete an expense
    ttk.Button(text = 'DELETE', command = db_op.delete_expense).grid(row = 5, column = 0, sticky = W + E)
    # Button to edit an expense
    ttk.Button(text = 'EDIT', command = db_op.edit_expense).grid(row = 5, column = 1, sticky = W + E)

    # Filling the rows
    db_op.get_expenses()

    window.mainloop()