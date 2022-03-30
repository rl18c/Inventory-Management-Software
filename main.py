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


def set_dat():
    # Functionally basic set statement, that ensures that product names and barcodes are unique.
    # Plan on implementing more in depth additive quantities or something similar later and
    # potentially more data.
    name = input("Insert name: ")
    x = Inventory.find_one({"name": name})
    if x:
        found = input("An item with this name exists. Would you like to modify it? (y/n):").lower()
        if found == "y":
            bcode = input("Insert barcode number: ")
            quan = input("Insert quantity: ")
            price = input("Insert price: ")
            if bcode == Inventory.find_one({"name": name})["barcode"]:
                Stats.insert_one({"time": datetime.datetime.now(), "barcode": bcode, "quantity": int(quan)})
            else:
                for item in x:
                    item["barcode"] = bcode
                Stats.insert_one({"time": datetime.datetime.now(), "barcode": bcode, "quantity": int(quan)})
            return Inventory.update_one({"name": name}, {"$set": {"name": name, "barcode": bcode,
                                                                  "quantity": int(quan), "price": float(price)}})
    bcode = input("Insert barcode number: ")
    y = Inventory.find_one({"barcode": bcode})
    if y:
        found = input("An item with this barcode exists. Would you like to modify it? (y/n):").lower()
        if found == "y":
            quan = input("Insert quantity: ")
            price = input("Insert price: ")
            Stats.insert_one({"time": datetime.datetime.now(), "barcode": bcode, "quantity": int(quan)})
            return Inventory.update_one({"barcode": bcode}, {"$set": {"name": name, "barcode": bcode,
                                                                      "quantity": int(quan), "price": float(price)}})

    # Below determines if the unique barcode is in the barcode name database, if it isn't, asks the user if they'd like
    # to add it (WANT TO OPTIMIZE THIS LATER)
    z = NameBcode.find_one({"barcode": bcode})
    if not z:
        found2 = input("Unique barcode found. Add to barcode DB? (y/n):").lower()
        if found2 == "y":
            NameBcode.insert_one({"name": name, "barcode": bcode})

    # Return to standard input for query
    quan = input("Insert quantity: ")
    price = input("Insert price: ")
    Stats.insert_one({"time": datetime.datetime.now(), "barcode": bcode, "quantity": int(quan)})
    return Inventory.insert_one({"name": name, "barcode": bcode, "quantity": int(quan), "price": float(price)})


def edit_dat():
    # NOT IMPLEMENTED
    return 0


# Simple Quantity editor for testing matplotlib functions
def edit_quan():
    typeIn = input("\nID by (N)ame or (B)arcode: ").lower()  # may change this to just input bar/name
    if typeIn == "n":
        name = input("Insert item name: ")
        item = Inventory.find_one({"name": name})
        if item:
            quantity = int(input("Insert new quantity as integer: "))
            Stats.insert_one({"time": datetime.datetime.now(), "barcode": item["barcode"], "quantity": quantity})
            return Inventory.update_one({"name": name}, {"$set": {"quantity": quantity}})
        else:
            print("Error: Couldn't find name.")
            return 0
    elif typeIn == "b":
        barcode = input("Insert item barcode: ")
        item = Inventory.find_one({"barcode": barcode})
        if item:
            quantity = int(input("Insert new quantity as integer: "))
            Stats.insert_one({"time": datetime.datetime.now(), "barcode": barcode, "quantity": quantity})
            return Inventory.update_one({"barcode": barcode}, {"$set": {"quantity": quantity}})
        else:
            print("Error: Couldn't find barcode.")
            return 0
    else:
        print("Error: Invalid type")
        return 0


def del_dat():
    name_bar = input("Insert name/barcode of item to be removed:")
    return Inventory.delete_one({"$or": [{"name": name_bar}, {"barcode": name_bar}]})


# !! SORT NOT WORKING, UNSURE AS TO WHY
def sort_dat():
    print("What would you like to sort by?")
    sort = input("(N)ame, (B)arcode, (Q)uantity, (P)rice:").lower()
    asOdes = input("(A)scending or (D)escending order:").lower()
    j = 0
    if sort == "n":
        if asOdes == "a":
            sorted = Inventory.find().sort("name")
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        elif asOdes == "d":
            sorted = Inventory.find().sort("name", -1)
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "b":
        if asOdes == "a":
            sorted = Inventory.find().sort("barcode")
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        elif asOdes == "d":
            sorted = Inventory.find().sort("barcode", -1)
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "q":
        if asOdes == "a":
            sorted = Inventory.find().sort("quantity")
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        elif asOdes == "d":
            sorted = Inventory.find().sort("quantity", -1)
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "p":
        if asOdes == "a":
            sorted = Inventory.find().sort("price")
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        elif asOdes == "d":
            sorted = Inventory.find().sort("price", -1)
            for i in sorted:
                j += 1
                print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                      + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
        else:
            print("Error: invalid input for Ascending/Descending.")
    else:
        print("Error: invalid input for sort type.")

    return


def get_stats(code):
    statsDict = Stats.find({"barcode": code})
    times = []
    quantities = []
    for i in statsDict:
        times.append(i["time"])
        quantities.append(i["quantity"])
    fig, ax = plt.subplots()
    ax.plot(times, quantities)
    item = NameBcode.find_one({"barcode": code})

    plt.title("Inventory of " + item["name"] + " Over Time")
    plt.ylabel("Quantity")
    plt.xlabel("Date/Time")
    plt.gcf().autofmt_xdate()
    plt.show()
    return 0


# ONLY USED FOR TESTING
def clear_dat():
    Inventory.delete_many({})
    Stats.delete_many({})
    NameBcode.delete_many({})


# Test function for testing matplotlib output in tandem with the databases.
def test_graphs():
    clear_dat()
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 31)
    d = datetime.timedelta(days=2)
    NameBcode.insert_one({"name": "TEST", "barcode": "0"})
    while start <= end:
        Stats.insert_one({"time": str(start), "barcode": "0", "quantity": random.randrange(0, 20)})
        start += d
    get_stats("0")
    clear_dat()


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

        # Populating with test data
        for e in test_entries:
            self.tree.insert("", END, values=e)

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
        b = self.n_str.get()
        q = int(self.q_str.get())
        p = float(self.rp_str.get())
        x = Inventory.find_one({"name": n})
        if x:
            nameF = tk.messagebox.askquestion \
                ('Name Found', 'Entry with name ' + n + ' found. Update it?')
            if nameF:
                Inventory.update_one({"name": n}, {"$set": {"name": n, "barcode": b,
                                                            "quantity": q,
                                                            "price": p}})
        y = Inventory.find_one({"barcode": b})
        if y and not x:
            nameB = tk.messagebox.askquestion \
                ('Barcode Found', 'Entry with barcode ' + b + ' found. Update it?')
            if nameB:
                Inventory.update_one({"barcode": b}, {"$set": {"name": n, "barcode": b,
                                                               "quantity": q,
                                                               "price": p}})
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
            Inventory.insert_one({"name": n, "barcode": b, "quantity": q, "price": p})

        Stats.insert_one({"time": datetime.datetime.now(), "barcode": b, "quantity": q})

        tk.messagebox.showinfo(
            title='Success',
            message="Value Successfully inserted!"
        )
        self.n_str.set("")
        self.b_str.set("")
        self.q_str.set("")
        self.rp_str.set("")

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
    print("Welcome to INVENTORY MANAGER testing.")
    while True:
        print("\nWhat would you like to do?")
        print("P: Print data")
        print("A: Add data")
        print("R: Remove data")
        print("S: Sort data")
        print("Q: Edit quantity of item")
        print("G: Show graph of item over time")
        print("C: Clear ALL data (Clears all 3 databases)")
        print("T: Run test function (CAUTION: CLEARS DATABASES)")
        print("X: Exit")
        inp = input().lower()
        if inp == "p":
            print("\nWhich database would you like to view?")
            print("[1] Inventory")
            print("[2] Statistics")
            print("[3] Unique Barcodes")
            response = input()
            if int(response) == 1:
                result = get_dat(Inventory)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                          + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
            elif int(response) == 2:
                result = get_dat(Stats)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Barcode: " + i['barcode'] + ", Time: " + str(i['time'])
                          + ", Quantity: " + str(i['quantity']))
            elif int(response) == 3:
                result = get_dat(NameBcode)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode'])
            else:
                print("Error: Invalid Database")
        elif inp == "a":
            result = set_dat()

        elif inp == "r":
            result = del_dat()

        elif inp == "s":
            sort_dat()

        elif inp == "q":
            result = edit_quan()

        elif inp == "g":
            bcode = input("\nInsert the barcode of the item to view: ")
            x = Stats.find_one({"barcode": bcode})
            if x:
                result = get_stats(bcode)
            else:
                print("Error: No barcode with that information found")

        elif inp == "c":
            clear_dat()

        elif inp == "t":
            test_graphs()

        elif inp == "x":
            sys.exit()
        else:
            print(inp + " = Invalid input. Try again.")


