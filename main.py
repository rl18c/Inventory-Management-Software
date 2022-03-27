# !!NOTE: FOR TESTING PURPOSES AND THIS EARLY VERSION, ALL INPUT OUTPUT WILL BE DONE IN CONSOLE.
# !!THIS SHOULD BE TRANSFERRED TO UI ONCE WE BEGIN TO IMPLEMENT IT.


# Main DB (Inventory) stores data in the format name: string, barcode: string, quantity: int, price: float
# Secondary DB (Stats) stores data in the form: barcode:string, time:datetime, quantity:int
# Tertiary DB (NameBcode) stores data in the form: name:string, barcode:string
import datetime
import random
import sys
import pymongo
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import *

client = pymongo.MongoClient("mongodb+srv://pygroup:rcagroup@project.uxruw.mongodb.net/InvManager")
db = client["InvManager"]
Inventory = db["Inventory"]
Stats = db["StatsTime"]  # Used in determining stats over time for the inventory
NameBcode = db["NameBarcode"]


def getDat(Collection):
    dicts = []
    for x in Collection.find():
        dicts.append(x)
    return dicts


def setDat():
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


def editDat():
    # NOT IMPLEMENTED
    return 0


# Simple Quantity editor for testing matplotlib functions
def editQuan():
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


def delDat():
    name_bar = input("Insert name/barcode of item to be removed:")
    return Inventory.delete_one({"$or": [{"name": name_bar}, {"barcode": name_bar}]})


# !! SORT NOT WORKING, UNSURE AS TO WHY
def sortDat():
    print("What would you like to sort by?")
    sort = input("(N)ame, (B)arcode, (Q)uantity, (P)rice:").lower()
    asOdes = input("(A)scending or (D)escending order:").lower()
    j = 0
    if sort == "n":
        if asOdes == "a":
            sorted  = Inventory.find().sort("name")
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


def getStats(code):
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
def clearDat():
    Inventory.delete_many({})
    Stats.delete_many({})
    NameBcode.delete_many({})


# Test function for testing matplotlib output in tandem with the databases.
def testGraphs():
    clearDat()
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 31)
    d = datetime.timedelta(days=2)
    NameBcode.insert_one({"name": "TEST", "barcode": "0"})
    while start <= end:
        Stats.insert_one({"time": str(start), "barcode": "0", "quantity": random.randrange(0, 20)})
        start += d
    getStats("0")
    clearDat()


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x600")
        self.title("Inventory Manager")
        self.resizable(0, 0)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.initialize_components()

    def initialize_components(self):
        # Title Label
        title_label = Label(self, text="Choose Option")
        title_label.grid(columnspan=2)

        # Show Inventory Button
        show_butt = Button(self, text="Show Inventory", command=self.inv_show)
        show_butt.grid(column=0, row=1)

        # Edit Data Button
        add_butt = Button(self, text="Add to Inventory", command=self.inv_add)
        add_butt.grid(column=0, row=2)

        # Close Window Button
        close_butt = Button(self, text="Close Manager", command=self.close_main)
        close_butt.grid(column=0, row=3)

    def inv_show(self):
        # This is where we must open new window to edit Inventory DB
        edit = Toplevel(self)

        edit.title("Data Modification")
        edit.geometry("200x200")

        def inv():
            output = ""
            res = getDat(Inventory)
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
            res = getDat(Stats)
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
            res = getDat(NameBcode)
            j = 0
            for i in res:
                j += 1
                output += ("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode'] + "\n")

            tk.messagebox.showinfo(
                title='Barcodes',
                message=output
            )

        # Add Label and Button to EDIT window
        mod_label = Label(edit, text="Which database Would you like to view?").grid(row=0)
        # out = Label(edit, text=output).grid(row=1)
        inv_butt = Button(edit, text="Inventory", command=lambda: inv())
        inv_butt.grid(row=1)
        stat_butt = Button(edit, text="Statistics", command=lambda: stat())
        stat_butt.grid(row=2)
        bcode_butt = Button(edit, text="Barcodes", command=lambda: barcode())
        bcode_butt.grid(row=3)
        back_butt = Button(edit, text="Go Back", command=lambda: self.close_edit(edit))
        back_butt.grid(row=4)

        # Hides Original window while modifying
        self.withdraw()


    def inv_add(self):
        # This is where we must open new window to edit Inventory DB
        edit = Toplevel(self)

        edit.title("Data Modification")
        edit.geometry("200x200")

        name = tk.StringVar()
        barcode = tk.StringVar()
        quantity = tk.StringVar()
        price = tk.StringVar()

        def submit_clicked():
            n = name.get()
            b = barcode.get()
            q = int(quantity.get())
            p = float(price.get())
            x = Inventory.find_one({"name": n})
            if x:
                nameF = tk.messagebox.askquestion\
                    ('Name Found','Entry with name ' + n + ' found. Update it?')
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
                        NameBcode.update_one({"barcode": b},{"$set": {"name": n, "barcode": b}})
                        Stats.delete_many({"barcode": b})
            if not x and not y:

                Inventory.insert_one({"name": n, "barcode": b, "quantity": q, "price": p})

            Stats.insert_one({"time": datetime.datetime.now(), "barcode": b, "quantity": q})

            tk.messagebox.showinfo(
                title='Success',
                 message="Value Successfully inserted!"
            )
            name_entry.delete(0, END)
            barc_entry.delete(0, END)
            quan_entry.delete(0, END)
            price_entry.delete(0, END)


        # name
        name_label = Label(edit, text="Product Name:")
        name_label.pack(fill='x', expand=True)

        name_entry = Entry(edit, textvariable=name)
        name_entry.pack(fill='x', expand=True)
        name_entry.focus()

        # barcode
        barc_label = Label(edit, text="Product Barcode:")
        barc_label.pack(fill='x', expand=True)

        barc_entry = Entry(edit, textvariable=barcode)
        barc_entry.pack(fill='x', expand=True)

        # quantity
        quan_label = Label(edit, text="Product Quantity:")
        quan_label.pack(fill='x', expand=True)

        quan_entry = Entry(edit, textvariable=quantity)
        quan_entry.pack(fill='x', expand=True)

        # price
        price_label = Label(edit, text="Product Price:")
        price_label.pack(fill='x', expand=True)

        price_entry = Entry(edit, textvariable=price)
        price_entry.pack(fill='x', expand=True)

        subm_butt = Button(edit, text="Submit", command=lambda: submit_clicked())
        subm_butt.pack(fill='x', expand=True)

        back_butt = Button(edit, text="Go Back", command=lambda: self.close_edit(edit))
        back_butt.pack(fill='x', expand=True)

        # Hides Original window while modifying
        self.withdraw()

    # Function used by EDIT's 'Go Back' button to close current and open original
    def close_edit(self, win):
        win.destroy()
        self.deiconify()

    def close_main(self):
        self.destroy()

    def greet(self):
        print("Greetings!")


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
                result = getDat(Inventory)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode']
                          + ", Quantity: " + str(i['quantity']) + ", Price: $" + str(i['price']))
            elif int(response) == 2:
                result = getDat(Stats)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Barcode: " + i['barcode'] + ", Time: " + str(i['time'])
                          + ", Quantity: " + str(i['quantity']))
            elif int(response) == 3:
                result = getDat(NameBcode)
                j = 0
                for i in result:
                    j += 1
                    print("[" + str(j) + "] " + "Name: " + i['name'] + ", Barcode: " + i['barcode'])
            else:
                print("Error: Invalid Database")
        elif inp == "a":
            result = setDat()

        elif inp == "r":
            result = delDat()

        elif inp == "s":
            sortDat()

        elif inp == "q":
            result = editQuan()

        elif inp == "g":
            bcode = input("\nInsert the barcode of the item to view: ")
            x = Stats.find_one({"barcode": bcode})
            if x:
                result = getStats(bcode)
            else:
                print("Error: No barcode with that information found")

        elif inp == "c":
            clearDat()

        elif inp == "t":
            testGraphs()

        elif inp == "x":
            sys.exit()
        else:
            print(inp + " = Invalid input. Try again.")
