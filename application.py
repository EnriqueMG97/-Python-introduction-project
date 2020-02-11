from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#-------------------------------------------------------------------------------------------------------#

import sqlite3
#-------------------------------------------------------------------------------------------------------#

import os

#-------------------------------------------------------------------------------------------------------#

import time

#-------------------------------------------------------------------------------------------------------#

import matplotlib.pyplot as plt
import numpy as np

#-------------------------------------------------------------------------------------------------------#
    
class Application(ttk.Frame):
    db_name =  'database.db'
    options = list()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Initializations
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.window.title('Expenses Control') 

        #-----------------------------------------------------------------------------------------------# (Right)

        # Frame container
        self.frame = LabelFrame(self.window, text = 'Enter a new expense')
        self.frame.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        # Inside the frame container

        #-----------------------------------------------------------------------------------------------# (Right)

        # Expenditure input
        # Label
        Label(self.frame, text = 'Expenditure: ').grid(row = 0, column = 0, pady = 5)
        # Writing box
        self.expenditure = Entry(self.frame)
        self.expenditure.focus()
        self.expenditure.grid(row = 0, column = 1, pady = 5)

        #-----------------------------------------------------------------------------------------------# (Right)

        # Price input
        # Label
        Label(self.frame, text = 'Price: ').grid(row = 1, column = 0, pady = 5)
        # Writing box
        self.price = Entry(self.frame)
        self.price.grid(row = 1, column = 1, pady = 5)

        #-----------------------------------------------------------------------------------------------# (Right)

        # Add expense
        ttk.Button(self.frame, text = 'Save Expense', command = self.add_expense).grid(row = 1, column = 3, padx = 5, pady = 5, sticky = W + E)

        #-----------------------------------------------------------------------------------------------# (Wrong)

        try:
            self.options = self.loadTags()
            self.saveTags()
        except FileNotFoundError:
            dir = os.getcwd() + '/tags.txt'
            file = open(dir, "w")
            file.close()

        # Tag selection
        # Label
        Label(self.frame, text = 'Tag: ').grid(row = 2, column = 0, pady = 5)
        # Tag menu
        self.combo = ttk.Combobox(self.frame, state = "readonly")
        self.combo.grid(row = 2, column = 1, pady = 5, sticky = W + E)
        self.combo['values'] = self.options

        #-----------------------------------------------------------------------------------------------# (Right)

        # Add tag
        ttk.Button(self.frame, text = 'Add Tag', command = self.tagMenu).grid(row = 2, column = 3, padx = 5, pady = 5, sticky = W + E)

        #-----------------------------------------------------------------------------------------------# (Not implemented totally)

        # Date selection
        # Label
        Label(self.frame, text = 'Date: ').grid(row = 3, column = 0, pady = 5)
        # Calendar (I do not know yet how to implement it, so meanwhile the date of the system)
        #ttk.Button(self.frame, text = 'Calendar').grid(row = 3, column = 1, pady = 5, sticky = W + E)
        self.date = time.strftime("%d/%m/%y")
        Entry(self.frame, textvariable = StringVar(self.frame, value = self.date), state = 'readonly').grid(row = 3, column = 1, pady = 5, sticky = W + E)

        #-----------------------------------------------------------------------------------------------# (Not implemented)

        # Import or export expenses data
        ttk.Button(text = "Import Expenses").grid(row = 1, column = 0, sticky = W + E)
        ttk.Button(text = 'Export Expenses').grid(row = 1, column = 1, sticky = W + E)

        #-----------------------------------------------------------------------------------------------# (Right)

        # Expenses data
        self.tree = ttk.Treeview(height = 20)
        self.tree.grid(row = 2, column = 0, columnspan = 2, pady = 5)
        self.tree["column"] = ["price", "tag", "date"]

        self.tree.heading('#0', text = 'Expenditure')
        self.tree.column('#0', anchor = 'center', width = 150)
        self.tree.heading('price', text = 'Price')
        self.tree.column('price', anchor = 'center', width = 150)
        self.tree.heading('tag', text = 'Tag')
        self.tree.column('tag', anchor = 'center', width = 150)
        self.tree.heading('date', text = 'Date')
        self.tree.column('date', anchor = 'center', width = 150)

        #-----------------------------------------------------------------------------------------------# (Right)

        # Delete or edit expenses data
        ttk.Button(text = 'Delete expense', command = self.delete_expense).grid(row = 3, column = 0, sticky = W + E)
        ttk.Button(text = 'Edit expense', command = self.edit_expense).grid(row = 3, column = 1, sticky = W + E)

        #-----------------------------------------------------------------------------------------------# (Not implemented)

        ttk.Button(text = 'See expense chart by month', command = self.month_chart).grid(row = 4, column = 0, columnspan = 2, pady = 5, sticky = W + E)

        #-----------------------------------------------------------------------------------------------#

        self.get_expenses()

#-------------------------------------------------------------------------------------------------------# (Right)
            
    def myMessage(self, e_title, e_message):
        messagebox.showerror(e_title, e_message)      

#-------------------------------------------------------------------------------------------------------# (Right)

    def tagMenu(self):
        self.tag_wind = Toplevel()
        self.tag_wind.title('Add Tag')
        Label(self.tag_wind, text = 'Add a new tag: ').grid(row = 0, column = 0)
        self.new_tag = Entry(self.tag_wind)
        self.new_tag.focus()
        self.new_tag.grid(row = 0, column = 1)
        ttk.Button(self.tag_wind, text = 'Save', command = self.addTag).grid(row = 1, column = 0, columnspan = 2, sticky = W + E)

    def addTag(self):
        aux = self.new_tag.get()
        tag = ""
        for i in range(len(aux)):
            if aux[i] == " ":
                tag += "_"
            else:
                tag += aux[i]
        if len(self.new_tag.get()) == 0:
            self.myMessage("Error!", "You can not save an empty tag")
        elif tag in self.options:
            self.myMessage("Error!", "The tag alredy exist")
        else:
            self.options += [tag]
            self.saveTags()
            self.combo['values'] = self.options

#-------------------------------------------------------------------------------------------------------# (Right)
    
    def loadTags(self):
        dir = os.getcwd() + '/tags.txt'
        file = open(dir, "r")
        query = 'SELECT DISTINCT tag FROM expenses'
        db_rows = self.run_query(query)
        tags = list()
        for row in db_rows:
            tags += row
        
        for element in file.read().split():
            if element not in tags:
                tags.append(element)
        return tags

#-------------------------------------------------------------------------------------------------------# (Right)
    
    def saveTags(self):
        dir = os.getcwd() + '/tags.txt'
        file = open(dir, "w")
        for element in self.options:
            file.write(element + " ")
        file.close()

#-------------------------------------------------------------------------------------------------------# (Right) (Minor error in the error message)

    # Get expenses from database
    def get_expenses(self):
        # Refresh the table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Filling table with data or creating a new one if there is none
        try:
            query = 'SELECT * FROM expenses'
            db_rows = self.run_query(query)
            for row in db_rows:
                self.tree.insert('', "end", text = row[1], values = (row[2], row[3], row[4], row[0]))
        except sqlite3.OperationalError:
            #self.myMessage("Error!", "No DB found. A new DB has been created")
            dir = os.getcwd() + '/database.db'
            file = open(dir, "w")
            file.close()      
            # Create a new DB
            con = sqlite3.connect(dir)
            cursor = con.cursor()
            cursor.execute('''CREATE TABLE "expenses"
                ("id"	        INTEGER     NOT NULL    UNIQUE,
	            "expenditure"	TEXT        NOT NULL,
	            "price"	        REAL        NOT NULL,
                "tag"	        TEXT,
	            "date"	        TEXT        NOT NULL,
	            PRIMARY KEY("id"))''')
            self.get_expenses()

#-------------------------------------------------------------------------------------------------------# (Right)

    # Return the DB data
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result     

#-------------------------------------------------------------------------------------------------------# (Right)

    def add_expense(self):
        if self.validation(self.expenditure.get(), self.price.get()):
            query = 'INSERT INTO expenses VALUES(NULL, ?, ?, ?, ?)'
            if len(self.combo.get()) == 0:
                self.combo.set("Other")
            try:
                parameters =  (self.expenditure.get(), float(self.price.get()), self.combo.get(), self.date)
                self.run_query(query, parameters)
                self.myMessage('Done!', 'Expense {} added successfully'.format(self.expenditure.get()))
                # Cleaning the input
                self.expenditure.delete(0, END)
                self.price.delete(0, END)
            except ValueError:
                self.myMessage('Error!', 'The price must be a real number')
                self.price.delete(0, END)
                return
        else:
            self.myMessage('Error!', 'Expediture and price is required')
            return
        self.get_expenses()

    # User input validation
    def validation(self, expenditure, price):
        return len(expenditure) != 0 and len(price) != 0

#-------------------------------------------------------------------------------------------------------# (Right)

    def delete_expense(self):
        try:
           self.tree.item(self.tree.selection())['values'][3]
        except IndexError:
            self.myMessage('Error!', 'Please select an expense')
            return
        expenditure = self.tree.item(self.tree.selection())['values'][3]
        query = 'DELETE FROM expenses WHERE id = ?'
        self.run_query(query, (str(expenditure), ))
        self.myMessage('Done!', 'Expense {} deleted successfully'.format(self.tree.item(self.tree.selection())['text']))
        self.get_expenses()

#-------------------------------------------------------------------------------------------------------# (Right) (Minor error in the button 'update')

    def edit_expense(self):
        try:
            id = self.tree.item(self.tree.selection())['values'][3]
        except IndexError:
            self.myMessage('Error!', 'Please select an expense')
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit expense'
        # Old Name
        Label(self.edit_wind, text = 'Old name: ').grid(row = 0, column = 1, pady = 5)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_name), state = 'readonly').grid(row = 0, column = 2, pady = 5)
        # New Name
        Label(self.edit_wind, text = 'New name:').grid(row = 1, column = 1, pady = 5)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2, pady = 5)
        # Old Price 
        Label(self.edit_wind, text = 'Old price:').grid(row = 2, column = 1, pady = 5)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2, pady = 5)
        # New Price
        Label(self.edit_wind, text = 'New price:').grid(row = 3, column = 1, pady = 5)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2, pady = 5)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_expenditure(new_name.get(), old_name, new_price.get(), old_price, id)).grid(row = 4, column = 1,columnspan = 2, sticky = W + E)

    def edit_expenditure(self, new_name, old_name, new_price, old_price, id):
        if self.validation(new_name, new_price):
            try:
                new_price = float(new_price)
                query = 'UPDATE expenses SET expenditure = ?, price = ? WHERE expenditure = ? AND price = ? AND id = ?'
                parameters = (new_name, new_price, old_name, old_price, id)
                self.run_query(query, parameters)
                self.myMessage('Done!', 'Expense {} updated successfully'.format(old_name))
                self.edit_wind.destroy()
                self.get_expenses()
            except ValueError:
                self.myMessage('Error!', 'The price must be a real number')
                return
        else:
            self.myMessage('Error!', 'Introduce the new name and the new price')
            return

#-------------------------------------------------------------------------------------------------------#

    def month_chart(self):
        month = list()
        actual_month = int(time.strftime("%m"))
        # We will see the actual month and the previous two
        for _ in range(3):
            if actual_month == 0:
                actual_month = 12
            # In each iteration we select the expenses of a month and we group them by the tags
            if actual_month >= 1 and actual_month <= 9:
                query = "SELECT SUM(price), tag FROM expenses WHERE date LIKE '%/0{}/%' GROUP BY tag".format(actual_month)
            else:
                query = "SELECT SUM(price), tag FROM expenses WHERE date LIKE '%/{}/%' GROUP BY tag".format(actual_month)
                
            # Here we have the total of each tag in each month
            db_rows = self.run_query(query)
            print(self.months[actual_month - 1])
            for row in db_rows:
                month.append(self.months[actual_month - 1])
                print(row[0], row[1])

            actual_month -= 1       

#-------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    window = Tk()
    application = Application(window)
    window.mainloop()