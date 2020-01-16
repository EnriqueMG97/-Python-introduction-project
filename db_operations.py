import sqlite3

class DB_Operations:

    db_name =  'database.db'

    # Initializations
    def __init__(self, expenditure, price, message, tree):
        self.expenditure = expenditure
        self.price = price
        self.message = message
        self.tree = tree
    
    # Function to execute database querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get expenses from database
    def get_expenses(self):
        # Cleaning the table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Getting data
        query = 'SELECT * FROM expenses ORDER BY expenditure DESC'
        db_rows = self.run_query(query)

        # Filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # User input validation
    def validation(self):
        return len(self.expenditure.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO expenses VALUES(NULL, ?, ?)'
            parameters =  (self.expenditure.get(), self.price.get())
            self.run_query(query, parameters)
            # COMO PONGO COMILLAS SIMPLES ENTRE LOS CORCHETES????
            self.message['text'] = 'Expense {} added successfully'.format(self.expenditure.get())
            #self.expenditure.delete(0, END)
            #self.price.delete(0, END)
        else:
            self.message['text'] = 'Expediture and price is required'
        self.get_expenses()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a expense'
        self.message['text'] = ''
        expenditure = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM expenses WHERE expenditure = ?'
        self.run_query(query, (expenditure, ))
        self.message['text'] = 'Expense {} deleted successfully'.format(expenditure)
        self.get_expenses()
