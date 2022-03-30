# !!NOTE: FOR TESTING PURPOSES AND THIS EARLY VERSION, ALL INPUT OUTPUT WILL BE DONE IN CONSOLE.
# !!THIS SHOULD BE TRANSFERRED TO UI ONCE WE BEGIN TO IMPLEMENT IT.


# Main DB (Inventory) stores data in the format name: string, barcode: string, quantity: int, price: float
# Secondary DB (Stats) stores data in the form: barcode:string, time:datetime, quantity:int
# Tertiary DB (NameBcode) stores data in the form: name:string, barcode:string
import datetime
import random
import sys
from tkinter import ttk
import pymongo
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import *

client = pymongo.MongoClient("mongodb+srv://pygroup:rcagroup@project.uxruw.mongodb.net/InvManager")

db = client["InvManager"]
Inventory = db["Inventory"]
Stats = db["StatsTime"]  # Used in determining stats over time for the inventory
NameBcode = db["NameBarcode"]


def get_dat(collection):
    dicts = []
    for x in collection.find():
        dicts.append(x)
    return dicts

def inv():
    output = ""
    res = get_dat(Inventory)
    j = 0
    for i in res:
        j += 1
        output += ("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                   + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']) + "\n")

    tk.messagebox.showinfo(
        title='Inventory',
        message=output
    )


def stat():
    output = ""
    res = get_dat(Stats)
    j = 0
    for i in res:
        j += 1
        output += ("[" + str(j) + "] " + "Barcode: " + i['barcode'] + ", Time: " + str(i['time'])
                   + ", Quantity: " + str(i['quantity']) + "\n")

    tk.messagebox.showinfo(
        title='Statistics',
        message=output
    )


def barcode():
    output = ""
    res = get_dat(NameBcode)
    j = 0
    for i in res:
        j += 1
        output += ("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode'] + "\n")

    tk.messagebox.showinfo(
        title='Barcodes',
        message=output
    )


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x220")
        self.title("Inventory Manager")
        self.resizable(False, False)
        self.configure(bg="#d0fbff")

        # Initializes label and buttons on main screen
        self.initialize_components()

        col, row = self.grid_size()
        for c in range(col):
            self.grid_columnconfigure(c, minsize=100)

    def initialize_components(self):
        # Title Label
        title_label = Label(self, text="Select an Action",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        title_label.grid(row=0, column=1, columnspan=3, sticky=EW, pady=10)

        # HERE WE DEFINE 4 FRAMES TO ACT AS BUTTON BORDERS
        # Button Frame 1
        but1_border = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        but1_border.grid(column=0, row=1, columnspan=2, sticky=W, padx=25, pady=10)
        # Button Frame 2
        but2_border = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        but2_border.grid(column=0, row=3, columnspan=2, sticky=W, padx=25, pady=10)
        # Button Frame 3
        but3_border = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        but3_border.grid(column=0, row=5, columnspan=2, sticky=W, padx=25, pady=10)
        # Button Frame 4
        but4_border = Frame(self, highlightthickness=2, highlightbackground="#d10000")
        but4_border.grid(column=3, row=5, columnspan=2, padx=25)

        # Add Data Button
        add_butt = Button(but1_border, text="Add to Inventory",
                          bg="white",
                          borderwidth=0,
                          font=("Helvetica", 11),
                          command=self.inv_add)
        add_butt.grid()
        add_butt.config(width=18)

        # Show Inventory Button
        show_butt = Button(but2_border, text="Show Inventory",
                           bg="white",
                           font=("Helvetica", 11),
                           borderwidth=0)
        show_butt.grid()
        show_butt.config(width=18)

        # Modify Button
        mod_butt = Button(but3_border, text="Modify Inventory", command=self.inv_edit,
                           bg="white",
                           font=("Helvetica", 11),
                           borderwidth=0)
        mod_butt.grid()
        mod_butt.config(width=18)

        # Close Window Button
        close_butt = Button(but4_border, text="Close Manager",
                            bg="white",
                            font=("Helvetica", 11),
                            command=self.close_main,
                            borderwidth=0)
        close_butt.grid()

    def inv_edit(self):
        # Hides Original window while modifying
        self.withdraw()
        # This is where we must open new window to edit Inventory DB
        show = EditInv(self)

    def inv_add(self):
        print("Accessing Inventory...")

        # Hides Original window while modifying
        self.withdraw()

        # This is where we must open new window to edit Inventory DB
        addn = AddNew(self)

    def close_main(self):
        self.destroy()

# Testing Data
head = ["Name", "Barcode", "Quantity", "Price"]
test_entries = [
("Name1","Barcode1","Quantity1","Price1") ,
("Name2","Barcode2","Quantity2","Price2") ,
("Name3","Barcode3","Quantity3","Price3") ,
("Name4","Barcode4","Quantity4","Price4") ,
("Name5","Barcode5","Quantity5","Price5") ,
("Name6","Barcode6","Quantity6","Price6") ,
("Name7","Barcode7","Quantity7","Price7") ,
("Name8","Barcode8","Quantity8","Price8") ,
("Name9","Barcode9","Quantity9","Price9") ,
("Name10","Barcode10","Quantity10","Price10"),
("Name1","Barcode1","Quantity1","Price1") ,
("Name2","Barcode2","Quantity2","Price2") ,
("Name3","Barcode3","Quantity3","Price3") ,
("Name4","Barcode4","Quantity4","Price4") ,
("Name5","Barcode5","Quantity5","Price5") ,
("Name6","Barcode6","Quantity6","Price6") ,
("Name7","Barcode7","Quantity7","Price7") ,
("Name8","Barcode8","Quantity8","Price8") ,
("Name9","Barcode9","Quantity9","Price9") ,
("Name10","Barcode10","Quantity10","Price10")
]


class EditInv(tk.Tk):
    def __init__(self, mas):
        super().__init__()
        self.main_window = mas
        self.configure(bg="#d0fbff")
        self.title("Data Modification")
        self.resizable(False, False)

        # Initializes instance attributes
        self.main_frame = None
        self.tree = None
        self.text = None
        self.scroll = None

        # Initialize window components
        self.init_components()

        col, row = self.grid_size()
        for c in range(col):
            self.grid_columnconfigure(c, minsize=25)
        for r in range(row):
            self.grid_rowconfigure(r, minsize=20)
        # Add Label and Button to EDIT window
        #mod_label = Label(self, text="Which database Would you like to view?")
        #mod_label.grid(row=0)
        # out = Label(edit, text=output).grid(row=1)
        #inv_butt = Button(self, text="Inventory", command=lambda: inv())
        #inv_butt.grid(row=1)
        #stat_butt = Button(self, text="Statistics", command=lambda: stat())
        #stat_butt.grid(row=2)
        #bcode_butt = Button(self, text="Barcodes", command=lambda: barcode())
        #bcode_butt.grid(row=3)
        #back_butt = Button(self, text="Go Back", command=self.close_win)
        #back_butt.grid(row=4)

    def init_components(self):
        # Create db_list outer frame
        self.main_frame = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(column=1, row=0, columnspan=5, rowspan=16, sticky=W, padx=25, pady=10)

        # Create text area for db entries
        self.tree = ttk.Treeview(self.main_frame, columns=head, show="headings",
                                 selectmode="browse",
                                 height=16)
        self.tree.column("Name", anchor=CENTER, width=80)
        self.tree.column("Barcode", anchor=CENTER, width=80)
        self.tree.column("Quantity", anchor=CENTER, width=80)
        self.tree.column("Price", anchor=CENTER, width=80)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=0, column=2, sticky="nsew", pady=2, padx=2)

        data = get_dat(Inventory)
        # Populating with database data
        for d in data:
            l = (d["name"], d["barcode"], str(d["quantity"]), str(d["r_price"]))
            self.tree.insert("", END, values=l)


        # Create scrollbar on right side
        self.scroll = Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=0, column=5, rowspan=16, sticky="nse")
        self.tree.config(yscrollcommand=self.scroll.set)

        # Create and place 'Remove' and 'Modify' buttons
        rem_butt = Button(self, text="Remove Selected Item")
        rem_butt.grid(row=17, column=1, rowspan=2, columnspan=2, sticky=W)

        mod_butt = Button(self, text="Modify Selected Item")
        mod_butt.grid(row=17, column=4, rowspan=2, columnspan=2, sticky=W)

        # Create Update Item button
        up_butt = Button(self, text="Update Item", state="disabled")

        back_butt = Button(self, text="Go Back", command=self.close_win)
        back_butt.grid(row=17, column=10, rowspan=2, columnspan=2, padx=20)

    def close_win(self):
        self.main_window.deiconify()
        self.destroy()


class AddNew(tk.Tk):
    def __init__(self, mas):
        super().__init__()
        self.main_window = mas
        self.configure(bg="#d0fbff")
        self.title("New Item")
        #self.geometry("330x300")
        self.resizable(False, False)

        # Creating 4 string variables for text box values
        self.n_str = StringVar(self)
        self.b_str = StringVar(self)
        self.q_str = StringVar(self)
        self.rp_str = StringVar(self)
        self.wp_str = StringVar(self)

        # Create frame to hold content of window
        b_frame = Frame(self)
        b_frame.grid(column=0, row=0, columnspan=5, rowspan=20, padx=25)
        b_frame.configure(bg="#d0fbff")

        # Title Label
        t_lbl = Label(b_frame, text="New Item Form",
                      font=("Helvetica", 16),
                      borderwidth=2,
                      relief="ridge",
                      bg="#d0fbff")
        t_lbl.grid(row=0, column=1, rowspan=2, columnspan=3, pady=15, sticky=W)

        # Create 4 labels for entry boxes
        n_lbl = Label(b_frame, text="Name >", font=("Helvetica", 11), bg="#d0fbff")
        n_lbl.grid(row=2, column=0, sticky=E)
        b_lbl = Label(b_frame, text="Barcode >", font=("Helvetica", 11), bg="#d0fbff")
        b_lbl.grid(row=5, column=0, sticky=E)
        q_lbl = Label(b_frame, text="Quantity >", font=("Helvetica", 11), bg="#d0fbff")
        q_lbl.grid(row=8, column=0, sticky=E)
        rp_lbl = Label(b_frame, text="Retail Price >", font=("Helvetica", 11), bg="#d0fbff")
        rp_lbl.grid(row=11, column=0, sticky=E)
        wp_lbl = Label(b_frame, text="Wholesale Price >", font=("Helvetica", 11), bg="#d0fbff")
        wp_lbl.grid(row=14, column=0, sticky=E)

        # Every time any entry text is changed,
        # check if all entry boxes have content (If they do enable add button)
        self.n_str.trace("w", self.ok_to_add)
        self.b_str.trace("w", self.ok_to_add)
        self.q_str.trace("w", self.ok_to_add)
        self.rp_str.trace("w", self.ok_to_add)
        self.wp_str.trace("w", self.ok_to_add)

        # Creating 5 entry boxes (Name - Barcode - Quantity - Retail Price - Wholesale Price)
        n_entry = Entry(b_frame, textvariable=self.n_str)
        n_entry.grid(row=2, column=1, columnspan=4, pady=15)
        b_entry = Entry(b_frame, textvariable=self.b_str)
        b_entry.grid(row=5, column=1, columnspan=4, pady=15)
        q_entry = Entry(b_frame, textvariable=self.q_str)
        q_entry.grid(row=8, column=1, columnspan=4, pady=15)
        rp_entry = Entry(b_frame, textvariable=self.rp_str)
        rp_entry.grid(row=11, column=1, columnspan=4, pady=15)
        wp_entry = Entry(b_frame, textvariable=self.wp_str)
        wp_entry.grid(row=14, column=1, columnspan=4, pady=15)
        # Add Item Button
        self.a_butt = Button(b_frame, text="Add Item",
                             state="disabled",
                             font=("Helvetica", 11),
                             command=self.db_add)
        self.a_butt.grid(row=17, column=0, columnspan=2, rowspan=2, pady=10, padx=15, sticky=W)

        # Go Back Button
        back_butt = Button(b_frame, text="Go Back", font=("Helvetica", 11),
                           command=self.close_win)
        back_butt.grid(row=17, column=4, columnspan=2, rowspan=2, pady=10, sticky=E)

        self.lift()

    def submit_clicked(self):
        n = self.n_str.get()
        b = self.b_str.get()
        q = int(self.q_str.get())
        rp = float(self.rp_str.get())
        wp = float(self.wp_str.get())
        x = Inventory.find_one({"name": n})
        if x:
            nameF = tk.messagebox.askquestion \
                ('Name Found', 'Entry with name ' + n + ' found. Update it?')
            if nameF:
                Inventory.update_one({"name": n}, {"$set": {"name": n, "barcode": b,
                                                            "quantity": q,
                                                            "r_price": rp, "w_price": wp}})
        y = Inventory.find_one({"barcode": b})
        if y and not x:
            nameB = tk.messagebox.askquestion \
                ('Barcode Found', 'Entry with barcode ' + b + ' found. Update it?')
            if nameB:
                Inventory.update_one({"barcode": b}, {"$set": {"name": n, "barcode": b,
                                                               "quantity": q,
                                                               "r_price": rp, "w_price": wp}})
        z = NameBcode.find_one({"barcode": b})
        if not z:
            nameBU = tk.messagebox.askquestion \
                ('Unique Barcode Found', 'Unique barcode found. Update unique database?')
            if nameBU:
                NameBcode.insert_one({"name": n, "barcode": b})
        else:
            if z["name"] != n:
                nameBA = tk.messagebox.askquestion \
                    ('Unique Barcode Already Used',
                     'Unique barcode already used. Update unique and statistics database?')
                if nameBA:
                    NameBcode.update_one({"barcode": b}, {"$set": {"name": n, "barcode": b}})
                    Stats.delete_many({"barcode": b})
        if not x and not y:
            Inventory.insert_one({"name": n, "barcode": b, "quantity": q, "r_price": rp, "w_price": wp})

        Stats.insert_one({"time": datetime.datetime.now(), "barcode": b, "quantity": q})

        tk.messagebox.showinfo(
            title='Success',
            message="Value Successfully inserted!"
        )
        self.n_str.set("")
        self.b_str.set("")
        self.q_str.set("")
        self.rp_str.set("")
        self.wp_str.set("")

    # Callback function for add item button
    def db_add(self):
        # Check that barcode==int && quantity==int && price==float (With at most 2 decimal places)
        if not self.b_str.get().isdigit():
            tk.messagebox.showerror(title="Invalid Barcode", message="Barcode must be comprised of only integers.")
            return
        if not self.q_str.get().isdigit():
            tk.messagebox.showerror(title="Invalid Quantity", message="Quantity must be a whole integer.")
            return
        try:
            float(self.rp_str.get())
            float(self.wp_str.get())
            if "." in self.rp_str.get() and len(self.rp_str.get().rsplit(".")[1]) > 2:
                raise ValueError
            if "." in self.rp_str.get() and len(self.rp_str.get().rsplit(".")[1]) < 2:
                raise ValueError
            if "." in self.wp_str.get() and len(self.wp_str.get().rsplit(".")[1]) > 2:
                raise ValueError
            if "." in self.wp_str.get() and len(self.wp_str.get().rsplit(".")[1]) < 2:
                raise ValueError
        except ValueError:
            tk.messagebox.showerror(title="Invalid Price",
                                    message="Price (Retail and Wholesale) must be a "
                                            "floating point number which "
                                            "does not extend beyond the "
                                            "hundredth place.")
            return
        # Here we have a valid item to get added
        self.submit_clicked()

    # Callback function for add item button
    def ok_to_add(self, var, index, mode):
        if self.n_str.get() and self.b_str.get() and self.q_str.get() and self.rp_str.get() and self.wp_str.get():
            self.a_butt.config(state="normal")
        else:
            self.a_butt.config(state="disabled")

    def close_win(self):
        self.main_window.deiconify()
        self.destroy()


if __name__ == '__main__':
    window = UI()
    window.mainloop()


