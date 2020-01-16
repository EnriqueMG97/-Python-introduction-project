from tkinter import *
    
class Window:

    # Initializations
    def __init__(self, window):
        self.window = window
        self.window.title('Expenses Control')

        # Creagting a Frame Container
        # Will create a frame in row 0 and that spans across columns 0, 1 and 2
        # and separated from the top edge 20 pixels
        self.frame = LabelFrame(self.window, text = 'Enter a new expense')
        self.frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Expenditure input
        Label(self.frame, text = 'Expenditure: ').grid(row = 1, column = 0)
        self.expenditure = Entry(self.frame)
        # It place the cursor over the text label
        self.expenditure.focus()
        self.expenditure.grid(row = 1, column = 1)

        # Price input
        Label(self.frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(self.frame)
        self.price.grid(row = 2, column = 1)

        # Output messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Expenditure', anchor = CENTER)
        self.tree.heading('#1', text = 'Price', anchor = CENTER)