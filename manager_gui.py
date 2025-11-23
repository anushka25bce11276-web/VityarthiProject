from tkinter import *
from tkinter import ttk, messagebox
from db_helper import RetailDB 
import datetime

class StoreManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Inventory Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        self.db = RetailDB()

        self.var_name = StringVar()
        self.var_cat = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        header_frame = Frame(self.root, bg="#333333", bd=2)
        header_frame.pack(side=TOP, fill=X)
        
        title_label = Label(header_frame, text="Store Inventory Management System", 
                            font=("Helvetica", 20, "bold"), fg="white", bg="#333333", pady=10)
        title_label.pack()

        input_frame = LabelFrame(self.root, text="Add New Item", font=("Arial", 12, "bold"), bg="#f0f0f0", bd=2, relief=GROOVE)
        input_frame.place(x=20, y=70, width=860, height=150)

        lbl_name = Label(input_frame, text="Item Name:", font=("Arial", 11), bg="#f0f0f0")
        lbl_name.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        entry_name = Entry(input_frame, textvariable=self.var_name, font=("Arial", 11), width=20)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        lbl_cat = Label(input_frame, text="Category:", font=("Arial", 11), bg="#f0f0f0")
        lbl_cat.grid(row=0, column=2, padx=15, pady=10, sticky="w")
        
        combo_cat = ttk.Combobox(input_frame, textvariable=self.var_cat, font=("Arial", 11), state="readonly", width=18)
        combo_cat['values'] = ("Electronics", "Clothing", "Home Decor", "Groceries", "Stationery")
        combo_cat.grid(row=0, column=3, padx=10, pady=10)
        combo_cat.current(0)

        lbl_price = Label(input_frame, text="Price (₹):", font=("Arial", 11), bg="#f0f0f0")
        lbl_price.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        entry_price = Entry(input_frame, textvariable=self.var_price, font=("Arial", 11), width=20)
        entry_price.grid(row=1, column=1, padx=10, pady=10)

        lbl_qty = Label(input_frame, text="Quantity:", font=("Arial", 11), bg="#f0f0f0")
        lbl_qty.grid(row=1, column=2, padx=15, pady=10, sticky="w")
        
        entry_qty = Entry(input_frame, textvariable=self.var_qty, font=("Arial", 11), width=20)
        entry_qty.grid(row=1, column=3, padx=10, pady=10)

        btn_frame = Frame(self.root, bg="#f0f0f0")
        btn_frame.place(x=20, y=230, width=860)

        btn_add = Button(btn_frame, text="Add Item", command=self.add_record, 
                         font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=15, height=2)
        btn_add.pack(side=LEFT, padx=20)

        btn_clear = Button(btn_frame, text="Clear Fields", command=self.clear_form, 
                           font=("Arial", 10, "bold"), bg="#FF9800", fg="white", width=15, height=2)
        btn_clear.pack(side=LEFT, padx=20)

        btn_del = Button(btn_frame, text="Delete Selected", command=self.delete_record, 
                         font=("Arial", 10, "bold"), bg="#F44336", fg="white", width=15, height=2)
        btn_del.pack(side=LEFT, padx=20)

        btn_exit = Button(btn_frame, text="Exit App", command=root.quit, 
                          font=("Arial", 10, "bold"), bg="#555", fg="white", width=15, height=2)
        btn_exit.pack(side=RIGHT, padx=20)

        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.place(x=20, y=300, width=860, height=280)

        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Category", "Price", "Qty", "Date"), show="headings", yscrollcommand=scroll_y.set)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Date", text="Date Added")

        self.tree.column("ID", width=40)
        self.tree.column("Name", width=200)
        self.tree.column("Category", width=120)
        self.tree.column("Price", width=80)
        self.tree.column("Qty", width=80)
        self.tree.column("Date", width=100)

        self.tree.pack(fill=BOTH, expand=1)
        
        self.load_data()

    def add_record(self):
        name = self.var_name.get()
        cat = self.var_cat.get()
        price = self.var_price.get()
        qty = self.var_qty.get()
        
        if name == "" or price == "" or qty == "":
            messagebox.showerror("Input Error", "Please fill in all the fields.")
            return

        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            self.db.add_item(name, cat, float(price), int(qty), current_date)
            
            messagebox.showinfo("Success", "Item added successfully!")
            self.clear_form()
            self.load_data()
        except ValueError:
            messagebox.showerror("Type Error", "Price and Quantity must be numbers.")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        rows = self.db.get_all_items()
        for row in rows:
            self.tree.insert("", END, values=row)

    def clear_form(self):
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_cat.set("Electronics") 

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return
        
        item_data = self.tree.item(selected_item)
        item_id = item_data['values'][0]
        
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
        if confirm:
            self.db.delete_item(item_id)
            self.load_data()

if __name__ == "__main__":
    root = Tk()
    app = StoreManager(root)
    root.mainloop()