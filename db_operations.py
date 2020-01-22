import sqlite3
from tkinter import *
import os

class DB_Operations:

    db_name =  'database.db'

    # Initializations
    def __init__(self, expenditure, price, message, tree):
        self.expenditure = expenditure
        self.price = price
        self.message = message
        self.tree = tree

    # Get expenses from database
    def get_expenses(self):
        # Cleaning the table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Getting data
        try:
            query = 'SELECT * FROM expenses ORDER BY expenditure DESC'
            db_rows = self.run_query(query)
            # Filling data
            for row in db_rows:
                self.tree.insert('', 0, text = row[1], values = row[2])
        except sqlite3.OperationalError as e:
            self.message['text'] = 'No DB found. A new DB has been created'
            file = open("/Users/enrique/Introducción a Python/Trabajo/database.db", "w")
            file.close()

            con = sqlite3.connect("/Users/enrique/Introducción a Python/Trabajo/database.db")
            cursor = con.cursor()
            cursor.execute('''CREATE TABLE "expenses"
                    ("id"	        INTEGER     NOT NULL,
	                "expenditure"	TEXT        NOT NULL,
	                "price"	        REAL        NOT NULL,
	                PRIMARY KEY("id"))''')

            self.get_expenses
        

        

    # Function to execute database querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def add_expense(self):
        if self.validation():
            query = 'INSERT INTO expenses VALUES(NULL, ?, ?)'
            parameters =  (self.expenditure.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Expense {} added successfully'.format(self.expenditure.get())
            # Cleaning the input
            self.expenditure.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Expediture and price is required'
        self.get_expenses()

    # User input validation
    def validation(self):
        return len(self.expenditure.get()) != 0 and len(self.price.get()) != 0

    def delete_expense(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select an expense'
            return
        self.message['text'] = ''
        expenditure = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM expenses WHERE expenditure = ?'
        self.run_query(query, (expenditure, ))
        self.message['text'] = 'Expense {} deleted successfully'.format(expenditure)
        self.get_expenses()

    def edit_expense(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select an expense'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit expense'

        # Old Name
        Label(self.edit_wind, text = 'Old name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price 
        Label(self.edit_wind, text = 'Old price:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'New price:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_expenditure(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_expenditure(self, new_name, name, new_price, old_price):
        query = 'UPDATE expenses SET expenditure = ?, price = ? WHERE expenditure = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Expense {} updated successfully'.format(name)
        self.get_expenses()
        
