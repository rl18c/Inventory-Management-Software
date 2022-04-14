# !!NOTE: FOR TESTING PURPOSES AND THIS EARLY VERSION, ALL INPUT OUTPUT WILL BE DONE IN CONSOLE.
# !!THIS SHOULD BE TRANSFERRED TO UI ONCE WE BEGIN TO IMPLEMENT IT.


# Main DB (Inventory) stores data in the format name: string, barcode: string, quantity: int, price: float
# Secondary DB (Stats) stores data in the form: barcode:string, time:datetime, quantity:int
# Tertiary DB (NameBcode) stores data in the form: name:string, barcode:string
from datetime import datetime, timedelta
import random
import sys
from tkinter import ttk
import pymongo
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import tkinter as tk
from tkinter import *
import tkcalendar as cal
from collections import OrderedDict

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
        # self.geometry("500x220")
        self.title("Inventory Manager")
        self.resizable(False, False)
        self.configure(bg="#d0fbff")

        # Initializing all instance attributes
        # Init Buttons
        self.rem_butt = None
        self.mod_butt = None
        self.up_butt = None
        self.add_butt = None
        self.g_all_butt = None
        self.g_sel_butt = None
        self.close_butt = None

        # Init Editing widgets
        self.tree_frame = None
        self.entry_frame = None
        self.tree = None
        self.scroll = None
        # Entry Labels
        self.n_lbl = None
        self.b_lbl = None
        self.q_lbl = None
        self.rp_lbl = None
        self.wp_lbl = None
        # Entry boxes
        self.n_entry = None
        self.b_entry = None
        self.q_entry = None
        self.rp_entry = None
        self.wp_entry = None
        # Vars keeping track of modification state and Current working entry
        self.cur = None
        self.modifying = None
        # String Vars
        self.n_str = StringVar(self)
        self.b_str = StringVar(self)
        self.q_str = StringVar(self)
        self.rp_str = StringVar(self)
        self.wp_str = StringVar(self)

        # Initializes main screen
        self.init_buttons()
        self.init_edit_view()

        # Initially disable modification text_boxes
        self.disable_entries()

        col, row = self.grid_size()
        # for c in range(col):
        # self.grid_columnconfigure(c, minsize=30)

    def init_buttons(self):
        # Define 7 borders for each button
        # Remove button border
        rem_bord = Frame(self, highlightthickness=2, highlightbackground="#eb7d34")
        rem_bord.grid(column=0, row=20, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Modify button Border
        mod_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        mod_bord.grid(column=3, row=20, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Update button border
        up_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        up_bord.grid(column=6, row=20, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Add button border
        add_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        add_bord.grid(column=9, row=20, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Graph all button border
        g_all_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        g_all_bord.grid(column=11, row=6, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Graph selection button border
        g_sel_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        g_sel_bord.grid(column=11, row=10, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
        # Close button border
        close_bord = Frame(self, highlightthickness=2, highlightbackground="#d10000")
        close_bord.grid(column=11, row=0, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)

        # Adding buttons to frames

        # Remove button
        self.rem_butt = Button(rem_bord, text="Remove Selected Item",
                               bg="white",
                               font=("Helvetica", 11),
                               borderwidth=0,
                               command=self.db_remove)
        self.rem_butt.grid()
        self.rem_butt.config(width=18)

        # Modify Button
        self.mod_butt = Button(mod_bord, text="Modify Selected Item",
                               bg="white",
                               font=("Helvetica", 11),
                               borderwidth=0,
                               command=self.modify_clicked)
        self.mod_butt.grid()
        self.mod_butt.config(width=18)

        # Update Button
        self.up_butt = Button(up_bord, text="Update Item",
                              bg="white",
                              font=("Helvetica", 11),
                              borderwidth=0,
                              command=self.db_update)
        self.up_butt.grid()
        self.up_butt.config(width=18)

        # Add Data Button
        self.add_butt = Button(add_bord, text="Add New Item",
                               bg="white",
                               borderwidth=0,
                               font=("Helvetica", 11),
                               command=self.inv_add)
        self.add_butt.grid()
        self.add_butt.config(width=18)

        # Graph All button
        self.g_all_butt = Button(g_all_bord, text="Graph All",
                                 bg="white",
                                 borderwidth=0,
                                 font=("Helvetica", 11),
                                 command=self.graph_menu)
        self.g_all_butt.grid()
        self.g_all_butt.config(width=18)

        # Graph Selection button
        self.g_sel_butt = Button(g_sel_bord, text="Graph Selection", state="disabled",
                                 bg="white",
                                 borderwidth=0,
                                 font=("Helvetica", 11),
                                 command=lambda: self.graph_menu(str(self.tree.item(self.cur)["values"][1])))
        self.g_sel_butt.grid()
        self.g_sel_butt.config(width=18)

        # Close Manager Button
        self.close_butt = Button(close_bord, text="Close Manager",
                                 bg="white",
                                 font=("Helvetica", 11),
                                 command=self.close_main,
                                 borderwidth=0)
        self.close_butt.grid()
        self.close_butt.config(width=18)

    def init_edit_view(self):
        # Create db_list outer frame
        self.tree_frame = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid(column=1, row=3, columnspan=4, rowspan=15, sticky=W, padx=25, pady=10)

        # Create frame for updating an entry
        self.entry_frame = Frame(self, bg="#d0fbff")
        self.entry_frame.grid_rowconfigure(0, weight=1)
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid(column=6, row=3, columnspan=5, rowspan=15, sticky=W, padx=25, pady=10)

        # Create 5 labels for up_frame
        self.n_lbl = Label(self.entry_frame, text="Name >", font=("Helvetica", 11), bg="#d0fbff")
        self.n_lbl.grid(row=5, column=6, sticky=E)
        self.b_lbl = Label(self.entry_frame, text="Barcode >", font=("Helvetica", 11), bg="#d0fbff")
        self.b_lbl.grid(row=8, column=6, sticky=E)
        self.q_lbl = Label(self.entry_frame, text="Quantity >", font=("Helvetica", 11), bg="#d0fbff")
        self.q_lbl.grid(row=11, column=6, sticky=E)
        self.rp_lbl = Label(self.entry_frame, text="Retail Price >", font=("Helvetica", 11), bg="#d0fbff")
        self.rp_lbl.grid(row=14, column=6, sticky=E)
        self.wp_lbl = Label(self.entry_frame, text="Wholesale Price >", font=("Helvetica", 11), bg="#d0fbff")
        self.wp_lbl.grid(row=17, column=6, sticky=E)

        # Create Entry Information Label
        entry_lbl = Label(self.entry_frame, text="Current Entry Information", font=("Helvetica", 13), bg="#d0fbff")
        entry_lbl.grid(row=3, column=7, columnspan=3, rowspan=2, sticky=N)

        # Create Title Label for screen
        entry_lbl = Label(self, text="Inventory Tracker", font=("Helvetica", 20), bg="#d0fbff")
        entry_lbl.grid(row=0, column=2, columnspan=8, rowspan=2, sticky=S)

        # Create 5 Entry boxes for up_frame
        self.n_entry = Entry(self.entry_frame, textvariable=self.n_str)
        self.n_entry.grid(row=5, column=7, columnspan=4, pady=15)
        self.b_entry = Entry(self.entry_frame, textvariable=self.b_str)
        self.b_entry.grid(row=8, column=7, columnspan=4, pady=15)
        self.q_entry = Entry(self.entry_frame, textvariable=self.q_str)
        self.q_entry.grid(row=11, column=7, columnspan=4, pady=15)
        self.rp_entry = Entry(self.entry_frame, textvariable=self.rp_str)
        self.rp_entry.grid(row=14, column=7, columnspan=4, pady=15)
        self.wp_entry = Entry(self.entry_frame, textvariable=self.wp_str)
        self.wp_entry.grid(row=17, column=7, columnspan=4, pady=15)

        # Create text area for db entries
        self.tree = ttk.Treeview(self.tree_frame, columns=head, show="headings",
                                 selectmode="browse",
                                 height=16)
        # Define each column's width
        self.tree.column("Name", anchor=CENTER, width=80)
        self.tree.column("Barcode", anchor=CENTER, width=80)
        self.tree.column("Quantity", anchor=CENTER, width=70)
        self.tree.column("r_price", anchor=CENTER, width=75)
        self.tree.column("w_price", anchor=CENTER, width=95)

        # Define heading's text
        self.tree.heading("Name", text="Name")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("r_price", text="Retail Price")
        self.tree.heading("w_price", text="Wholesale Price")
        self.tree.grid(row=3, column=1, columnspan=4, sticky="nsew", pady=5, padx=5)
        # Binding a selection change to function
        self.tree.bind("<<TreeviewSelect>>", self.select_changed)

        data = get_dat(Inventory)
        # Populating with database data
        for d in data:
            l = (d["name"], d["barcode"], str(d["quantity"]), "$" + "{:.2f}".format(d["r_price"]),
                 "$" + "{:.2f}".format(d["w_price"]))
            self.tree.insert("", END, values=l)

        # Create scrollbar on right side
        self.scroll = Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=3, column=5, rowspan=16, sticky="nse")
        self.tree.config(yscrollcommand=self.scroll.set)

    # Called when 'Modify Selected Item' is clicked
    def modify_clicked(self):
        if self.cur:
            self.modifying = True
            self.enable_modifications()
        else:
            tk.messagebox.showerror(title="No Selection", message="No selected item to modify.")

    # Called everytime selection in treeview changes
    def select_changed(self, event):
        self.g_sel_butt["state"] = "normal"
        if self.modifying:
            if tk.messagebox.askyesno(title="Switch",
                                      message="Are you sure you want to terminate modifications?"):
                self.cur = self.tree.focus()
                i = self.tree.item(self.cur)
                self.n_str.set(i["values"][0])
                self.b_str.set(i["values"][1])
                self.q_str.set(i["values"][2])
                self.rp_str.set(i["values"][3][1:])
                self.wp_str.set(i["values"][4][1:])
                self.modifying = False
                self.disable_modifications()
        elif self.tree.focus():
            self.cur = self.tree.focus()
            i = self.tree.item(self.cur)
            self.n_str.set(i["values"][0])
            self.b_str.set(i["values"][1])
            self.q_str.set(i["values"][2])
            self.rp_str.set(i["values"][3][1:])
            self.wp_str.set(i["values"][4][1:])
        else:
            self.n_str.set("")
            self.b_str.set("")
            self.q_str.set("")
            self.rp_str.set("")
            self.wp_str.set("")

    # Called when user clicks Remove Item
    def db_remove(self):
        if self.cur:
            i = self.tree.item(self.cur)
            name_val = str(i["values"][0])
            bar_val = str(i["values"][1])

            Inventory.delete_one({"name": name_val, "barcode": bar_val})
            self.tree.delete(self.cur)
            del_unique = tk.messagebox.askquestion \
                ('Barcode', 'Delete name + barcode correlation?')
            if del_unique:
                NameBcode.delete_one({"name": name_val, "barcode": bar_val})
            del_stats = tk.messagebox.askquestion \
                ('Statistics', 'Delete statistic data for item?')
            if del_stats:
                Stats.delete_many({"barcode": bar_val})
            tk.messagebox.showinfo(title="Item Deletion",
                                   message="Item : " + name_val + " has been deleted.")
        else:
            tk.messagebox.showerror(title="No Selection", message="No selected item to remove.")

    # Called when user clicks Update Item
    def db_update(self):
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
        # Here we have a valid item to get added (MUST ADD AND SET modifying=false)
        i = self.tree.item(self.cur)
        n = str(self.n_str.get())
        b = str(self.b_str.get())
        q = int(self.q_str.get())
        rp = float(self.rp_str.get())
        wp = float(self.wp_str.get())
        # need to add checks for updating name/barcode and changing quantity for stats
        if q != int(i["values"][2]):
            Stats.insert_one(
                {"time": datetime.now(), "barcode": b, "quantity": q, "r_price": rp, "w_price": wp})
        if n != str(i["values"][0]) or b != str(i["values"][1]):

            name_update = tk.messagebox.askquestion \
                ('Unique Update', 'Name/Barcode changed: Update unique correlation?' + n + str(i["values"][0]))
            if name_update:
                barcode_update = False
                if NameBcode.find_one({"barcode": b}) and b != str(i["values"][1]):
                    barcode_update = tk.messagebox.askquestion \
                        ('Barcode Taken', 'Switch or delete barcodes? (Yes for modify, no for Delete)')
                    if barcode_update:
                        NameBcode.update_one({"barcode": b}, {"$set": {"barcode": str(i["values"][1])}})
                        Inventory.update_one({"barcode": b}, {"$set": {"barcode": str(i["values"][1])}})
                        Stats.update_many({"barcode": b}, {"$set": {"barcode": "placeholder"}})
                        # Column integer to match the column which was clicked in the table
                        entries = self.tree.get_children()

                        for item in entries:  # NEED TO UPDATE VIEW (this does not work)
                            if str(self.tree.item(item)['values'][1]) == b:
                                self.tree.item(item)['values'][1] = str(i["values"][1])
                                break

                    else:
                        NameBcode.delete_one({"barcode": b})
                        Inventory.delete_one({"barcode": b})
                        Stats.delete_many({"barcode": b})

                NameBcode.update_one({"name": str(i["values"][0])}, {"$set": {"name": n, "barcode": b}})
                Inventory.update_one({"name": str(i["values"][0])}, {"$set": {"name": n, "barcode": b,
                                                                              "quantity": q, "r_price": rp,
                                                                              "w_price": wp}})
                Stats.update_many({"barcode": str(i["values"][1])}, {"$set": {"barcode": b}})
                if barcode_update:
                    Stats.update_many({"barcode": "placeholder"}, {"$set": {"barcode": str(i["values"][1])}})
        Inventory.update_one({"name": str(i["values"][0]),
                              "barcode": str(i["values"][1])}, {"$set": {"name": n, "barcode": b,
                                                                         "quantity": q, "r_price": rp, "w_price": wp}})
        self.tree.item(self.cur, values=(n, b, str(q), '$' + "{:.2f}".format(rp), '$' + "{:.2f}".format(wp)))
        self.modifying = False
        self.disable_modifications()
        tk.messagebox.showinfo(title="Item Update",
                               message="Item : " + self.n_str.get() + " has been updated.")

    # Called when user want to modify something
    def enable_modifications(self):
        # Enable all entry boxes
        self.n_entry["state"] = "normal"
        self.b_entry["state"] = "normal"
        self.q_entry["state"] = "normal"
        self.rp_entry["state"] = "normal"
        self.wp_entry["state"] = "normal"
        # Enable Update Item button
        self.up_butt["state"] = "normal"
        # Disable all other buttons
        self.add_butt["state"] = "disabled"
        self.g_all_butt["state"] = "disabled"
        self.g_sel_butt["state"] = "disabled"
        self.mod_butt["state"] = "disabled"
        self.rem_butt["state"] = "disabled"

    # Called when user finishes modifications
    def disable_modifications(self):
        # Enable all other buttons
        self.add_butt["state"] = "normal"
        self.g_all_butt["state"] = "normal"
        self.g_sel_butt["state"] = "normal"
        self.mod_butt["state"] = "normal"
        self.rem_butt["state"] = "normal"
        # Disable entry boxes and Update button
        self.disable_entries()

    # Function to disable entry boxes and disable Update Item button
    def disable_entries(self):
        self.n_entry["state"] = "disabled"
        self.b_entry["state"] = "disabled"
        self.q_entry["state"] = "disabled"
        self.rp_entry["state"] = "disabled"
        self.wp_entry["state"] = "disabled"
        self.up_butt["state"] = "disabled"

    # Called by both Graphing Buttons
    def graph_menu(self, item_bcode=None):
        # Hides Original window while modifying
        if self.cur is not None:
            self.withdraw()
            graphm = GraphMenu(self, item_bcode)
        elif item_bcode is None:
            self.withdraw()
            graphm = GraphMenu(self, item_bcode)

    # Called by Add Item Button
    def inv_add(self):
        # Hides Original window while modifying
        self.withdraw()
        # This is where we must open new window to add Inventory DB
        addn = AddNew(self)

    def close_main(self):
        self.destroy()


# Testing Data
head = ["Name", "Barcode", "Quantity", "r_price", "w_price"]
test_entries = [
    ("Name1", "Barcode1", "Quantity1", "rPrice1", "wPrice1"),
    ("Name2", "Barcode2", "Quantity2", "rPrice2", "wPrice2"),
    ("Name3", "Barcode3", "Quantity3", "rPrice3", "wPrice3"),
    ("Name4", "Barcode4", "Quantity4", "rPrice4", "wPrice4"),
    ("Name5", "Barcode5", "Quantity5", "rPrice5", "wPrice5"),
    ("Name6", "Barcode6", "Quantity6", "rPrice6", "wPrice6"),
    ("Name7", "Barcode7", "Quantity7", "rPrice7", "wPrice7"),
    ("Name8", "Barcode8", "Quantity8", "rPrice8", "wPrice8"),
    ("Name9", "Barcode9", "Quantity9", "rPrice9", "wPrice9"),
    ("Name10", "Barcode10", "Quantity10", "rPrice10", "wPrice10"),
    ("Name1", "Barcode1", "Quantity1", "rPrice1", "wPrice1"),
    ("Name2", "Barcode2", "Quantity2", "rPrice2", "wPrice2"),
    ("Name3", "Barcode3", "Quantity3", "rPrice3", "wPrice3"),
    ("Name4", "Barcode4", "Quantity4", "rPrice4", "wPrice4"),
    ("Name5", "Barcode5", "Quantity5", "rPrice5", "wPrice5"),
    ("Name6", "Barcode6", "Quantity6", "rPrice6", "wPrice6"),
    ("Name7", "Barcode7", "Quantity7", "rPrice7", "wPrice7"),
    ("Name8", "Barcode8", "Quantity8", "rPrice8", "wPrice8"),
    ("Name9", "Barcode9", "Quantity9", "rPrice9", "wPrice9"),
    ("Name10", "Barcode10", "Quantity10", "rPrice10", "wPrice10")
]


class AddNew(tk.Tk):
    def __init__(self, mas):
        super().__init__()
        self.main_window = mas
        self.configure(bg="#d0fbff")
        self.title("New Item")
        # self.geometry("330x300")
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

        # Add button border
        add_border = Frame(b_frame, highlightthickness=2, highlightbackground="#37d3ff")
        add_border.grid(row=17, column=0, columnspan=2, rowspan=2, pady=10, padx=15, sticky=W)
        # Go Back button border
        back_border = Frame(b_frame, highlightthickness=2, highlightbackground="#d10000")
        back_border.grid(row=17, column=4, columnspan=2, rowspan=2, pady=10, sticky=E)

        # Add Item Button
        self.a_butt = Button(add_border, text="Add Item",
                             bg="white",
                             borderwidth=0,
                             state="disabled",
                             font=("Helvetica", 11),
                             command=self.db_add)
        self.a_butt.grid()

        # Go Back Button
        back_butt = Button(back_border, text="Go Back", font=("Helvetica", 11),
                           bg="white",
                           borderwidth=0,
                           command=self.close_win)
        back_butt.grid()

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
                    Inventory.update_one({"barcode": b}, {"$set": {"name": n, "barcode": b, "quantity": q,
                                                                   "r_price": rp, "w_price": wp}})
        if not x and not y:
            Inventory.insert_one({"name": n, "barcode": b, "quantity": q, "r_price": rp, "w_price": wp})

        Stats.insert_one({"time": datetime.now(), "barcode": b, "quantity": q, "r_price": rp, "w_price": wp})

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


class GraphMenu(tk.Tk):
    def __init__(self, mas, item_bcode=None):
        super().__init__()
        self.main_window = mas
        self.configure(bg="#d0fbff")
        self.title("Choose Option")
        # self.geometry("330x300")
        self.resizable(False, False)
        # Create frame to hold content of window
        self.popup_c = None
        self.popup_g = None
        # Initialize selections barcode
        self.sel_barcode = item_bcode
        b_frame = Frame(self)
        b_frame.grid(column=0, row=0, columnspan=5, rowspan=20, padx=25)
        b_frame.configure(bg="#d0fbff")

        # Title Label
        t_lbl = Label(b_frame, text="Graph Options",
                      font=("Helvetica", 16),
                      borderwidth=2,
                      relief="ridge",
                      bg="#d0fbff")
        t_lbl.grid(row=0, column=1, rowspan=2, columnspan=3, pady=15, sticky=W)
        # Stock button border
        s_border = Frame(b_frame, highlightthickness=2, highlightbackground="#37d3ff")
        s_border.grid(row=17, column=0, columnspan=2, rowspan=2, pady=10, padx=15, sticky=W)
        # Profit Graph Button
        p_border = Frame(b_frame, highlightthickness=2, highlightbackground="#37d3ff")
        p_border.grid(row=17, column=2, columnspan=2, rowspan=2, pady=10, padx=15, sticky=W)
        # Go Back button border
        back_border = Frame(b_frame, highlightthickness=2, highlightbackground="#d10000")
        back_border.grid(row=17, column=4, columnspan=2, rowspan=2, pady=10, sticky=E)

        # Stock Item Button
        self.s_butt = Button(s_border, text="Stock Graph",
                             bg="white",
                             borderwidth=0,
                             font=("Helvetica", 11),
                             command=self.stock_options)
        self.s_butt.grid()
        self.p_butt = Button(p_border, text="Profit Graph",
                             bg="white",
                             borderwidth=0,
                             font=("Helvetica", 11),
                             command=self.prof_options)
        self.p_butt.grid()

        # Go Back Button
        back_butt = Button(back_border, text="Go Back", font=("Helvetica", 11),
                           bg="white",
                           borderwidth=0,
                           command=self.close_win)
        back_butt.grid()

        self.lift()

    def stock_options(self):
        if self.sel_barcode is None:
            self.calender_select(1, 0)
        else:
            self.calender_select(0, 0)

    def prof_options(self):
        if self.sel_barcode is None:
            self.calender_select(1, 1)
        else:
            self.calender_select(0, 1)

    def calender_select(self, typeA, typeB):
        self.popup_c = tk.Tk()
        self.popup_c.wm_title("Select a starting point")
        cal_day = datetime.now().date() - timedelta(days=7)
        calender = cal.Calendar(self.popup_c, selectmode='day',
                                year=cal_day.year, month=cal_day.month,
                                day=cal_day.day)

        calender.pack(pady=20)
        label = ttk.Label(self.popup_c, text="Select a starting date for the graph.")
        label.pack(side="top", fill="x", pady=10)
        if typeA == 1:
            b1 = ttk.Button(self.popup_c, text="Submit",
                            command=lambda: self.show_graph(calender.get_date(), typeA, typeB, self.sel_barcode))
        else:
            b1 = ttk.Button(self.popup_c, text="Submit",
                            command=lambda: self.show_graph(calender.get_date(), typeA, typeB, self.sel_barcode))
        b1.pack()
        self.popup_c.mainloop()

    def show_graph(self, day, typeA, typeB, code):
        self.popup_c.destroy()
        self.popup_g = tk.Tk()
        self.popup_g.configure(bg="#d0fbff")
        start = datetime.strptime(day, "%m/%d/%y")
        if typeB == 0:
            if typeA == 0:
                statsDict = Stats.find({"barcode": code})
                times = []
                quantities = []
                for i in statsDict:
                    if start <= i["time"] <= datetime.now():
                        times.append(i["time"])
                        quantities.append(i["quantity"])
                fig, ax = plt.subplots()
                ax.plot(times, quantities, zorder=1)
                ax.scatter(times, quantities, zorder=2, color='black')
                item = NameBcode.find_one({"barcode": code})
                self.popup_g.title('Inventory of ' + item["name"])
                plt.title("Inventory of " + item["name"] + " Over Time")
                plt.ylabel("Quantity")
                plt.xlabel("Date/Time")
                plt.grid()
                plt.gcf().autofmt_xdate()
                # plt.show()
                frame = tk.Frame(self.popup_g)
                canvas = FigureCanvasTkAgg(fig,
                                           master=frame)
                canvas.draw()
                NavigationToolbar2Tk(canvas, frame)
                # placing the canvas on the Tkinter window
                canvas.get_tk_widget().pack()
                frame.grid(column=1, row=2, columnspan=6, rowspan=17)

            else:
                bcodeDict = get_dat(NameBcode)
                times = []
                quantities = []

                fig, ax = plt.subplots()
                for j in bcodeDict:
                    statsDict = Stats.find({"barcode": j["barcode"]})
                    for i in statsDict:
                        if start <= i["time"] <= datetime.now():
                            times.append(i["time"])
                            quantities.append(i["quantity"])
                    plt.plot(times, quantities, zorder=1, label=str(j["name"]))
                    plt.scatter(times, quantities, zorder=2, color='black')
                    times.clear()
                    quantities.clear()

                self.popup_g.title('Inventory Overall')
                plt.title("Inventory Over Time")
                plt.ylabel("Quantity")
                plt.xlabel("Date/Time")
                plt.grid()
                plt.legend(loc='best')
                plt.gcf().autofmt_xdate()
                # plt.show()
                frame = tk.Frame(self.popup_g)
                canvas = FigureCanvasTkAgg(fig,
                                           master=frame)
                canvas.draw()
                NavigationToolbar2Tk(canvas, frame)
                # placing the canvas on the Tkinter window
                canvas.get_tk_widget().pack()
                frame.grid(column=1, row=2, columnspan=6, rowspan=17)
        else:
            if typeA == 0:
                statsDict = Stats.find({"barcode": code})
                times = [start.date()]
                profits = [0]
                overall = 0.0
                temp = 0
                for i in statsDict:
                    if start <= i["time"] <= datetime.now():
                        times.append(i["time"])
                        change = temp - i["quantity"]
                        if i["quantity"] < temp:
                            overall += float(change) * float(i["r_price"])
                            profits.append(overall)
                        elif i["quantity"] > temp:
                            overall += float(change) * float(i["w_price"])
                            profits.append(overall)

                        temp = i["quantity"]
                fig, ax = plt.subplots()
                for x1, x2, y1, y2 in zip(times, times[1:], profits, profits[1:]):
                    if y1 > y2:
                        ax.plot([x1, x2], [y1, y2], 'r')
                    elif y1 < y2:
                        ax.plot([x1, x2], [y1, y2], 'g')
                    else:
                        ax.plot([x1, x2], [y1, y2], 'b')
                ax.scatter(times, profits, zorder=2, color='black')
                item = NameBcode.find_one({"barcode": code})

                plt.suptitle("Profits of " + item["name"] + " Over Time")
                plt.ylabel("Profit")
                plt.xlabel("Date/Time")
                if overall >= 0:
                    plt.title("Overall Profit: $" + "{:.2f}".format(overall), color="green")
                else:
                    plt.title("Overall Loss: $" + "{:.2f}".format(overall), color="red")
                plt.gcf().autofmt_xdate()
                plt.grid()
                # plt.show()
                frame = tk.Frame(self.popup_g)
                canvas = FigureCanvasTkAgg(fig,
                                           master=frame)
                canvas.draw()
                NavigationToolbar2Tk(canvas, frame)
                # placing the canvas on the Tkinter window
                canvas.get_tk_widget().pack()
                frame.grid(column=1, row=2, columnspan=6, rowspan=17)
            else:
                bcodeDict = get_dat(NameBcode)
                times = [start.date()]
                profits = [0]
                profit_per = {}
                overall = 0.0
                overall_per = 0.0
                temp = 0
                # Iterate through database and locate
                for j in bcodeDict:
                    statsDict = Stats.find({"barcode": j["barcode"]})
                    for i in statsDict:
                        if start <= i["time"] <= datetime.now():
                            times.append(i["time"].date())
                            change = temp - i["quantity"]
                            if i["quantity"] < temp:
                                overall_per += float(change) * float(i["r_price"])
                                overall += float(change) * float(i["r_price"])
                                profits.append(overall)
                            elif i["quantity"] > temp:
                                overall_per += float(change) * float(i["w_price"])
                                overall += float(change) * float(i["w_price"])
                                profits.append(overall)

                            temp = i["quantity"]
                    profit_per[j["name"]] = overall_per
                    overall_per = 0.0
                    temp = 0

                # print individual values
                # sort dict
                sorted_p = {k: v for k, v in sorted(profit_per.items(), key=lambda item: item[1])}
                out = "Products ordered by value:"
                title = Label(self.popup_g, text=out, font=("Helvetica", 11),
                              bg="#d0fbff",
                              relief="groove",
                              borderwidth=3,
                              highlightcolor="#a8329e")
                title.grid(column=8, row=2, columnspan=2, sticky=EW)
                lbl_list = []
                i = 1
                for key, value in sorted_p.items():
                    t = "[" + str(i) + "] " + key + ": $" + "{:.2f}".format(value)
                    t_item = Label(self.popup_g, text=t, font=("Helvetica", 10), bg="#d0fbff")
                    t_item.grid(column=8, row=2 + i, columnspan=2, sticky=W)
                    # out += "[" + str(i) + "] " + key + ": $" + "{:.2f}\n".format(value)
                    i += 1

                # label = ttk.Label(self.popup_g, text=out)
                # label.pack(side="right", fill="x", pady=10)

                # sort data by date
                times, profits = zip(*sorted(zip(times, profits)))

                # Iterative loop to combine profits for values on the same day
                ordered = OrderedDict()
                for thing1, thing2 in zip(times, profits):
                    if ordered:
                        if thing1 in ordered.keys():
                            ordered[thing1] += thing2
                        else:
                            ordered[thing1] = thing2
                    else:
                        ordered[thing1] = thing2
                times = list(ordered.keys())
                profits = list(ordered.values())

                fig, ax = plt.subplots()
                # Plotting profits
                for x1, x2, y1, y2 in zip(times, times[1:], profits, profits[1:]):
                    if y1 > y2:
                        ax.plot([x1, x2], [y1, y2], 'r')
                    elif y1 < y2:
                        ax.plot([x1, x2], [y1, y2], 'g')
                    else:
                        ax.plot([x1, x2], [y1, y2], 'b')
                ax.scatter(times, profits, zorder=2, color='black')

                plt.suptitle("Overall Profits Over Time")
                plt.ylabel("Profit")
                plt.xlabel("Date/Time")
                if overall >= 0:
                    plt.title("Overall Profit: $" + "{:.2f}".format(overall), color="green")
                else:
                    plt.title("Overall Loss: $" + "{:.2f}".format(overall), color="red")
                plt.gcf().autofmt_xdate()
                plt.grid()
                # plt.show()
                plt.gcf().autofmt_xdate()
                # plt.show()
                frame = tk.Frame(self.popup_g)
                canvas = FigureCanvasTkAgg(fig,
                                           master=frame)
                canvas.draw()
                NavigationToolbar2Tk(canvas, frame)
                # placing the canvas on the Tkinter window
                canvas.get_tk_widget().pack()
                frame.grid(column=1, row=2, columnspan=6, rowspan=17)
        # Close button border
        close_bord = Frame(self.popup_g, highlightthickness=2, highlightbackground="#d10000")
        close_bord.grid(column=3, row=20, columnspan=2, rowspan=2, sticky=EW, padx=25, pady=12)
        b1 = Button(close_bord, text="Return to Graph Selection", command=self.close_win,
                    bg="white",
                    font=("Helvetica", 10),
                    borderwidth=0)
        b1.grid()

    def close_win(self):
        if self.popup_g is not None:
            self.popup_g.destroy()
            self.popup_g = None
        else:
            self.main_window.deiconify()
            self.destroy()


if __name__ == '__main__':
    window = UI()
    window.mainloop()
