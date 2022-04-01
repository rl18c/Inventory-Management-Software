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
head = ["Name", "Barcode", "Quantity", "r_price", "w_price"]
test_entries = [
("Name1","Barcode1","Quantity1","rPrice1", "wPrice1") ,
("Name2","Barcode2","Quantity2","rPrice2", "wPrice2") ,
("Name3","Barcode3","Quantity3","rPrice3", "wPrice3") ,
("Name4","Barcode4","Quantity4","rPrice4", "wPrice4") ,
("Name5","Barcode5","Quantity5","rPrice5", "wPrice5") ,
("Name6","Barcode6","Quantity6","rPrice6", "wPrice6") ,
("Name7","Barcode7","Quantity7","rPrice7", "wPrice7") ,
("Name8","Barcode8","Quantity8","rPrice8", "wPrice8") ,
("Name9","Barcode9","Quantity9","rPrice9", "wPrice9") ,
("Name10","Barcode10","Quantity10","rPrice10", "wPrice10"),
("Name1","Barcode1","Quantity1","rPrice1", "wPrice1") ,
("Name2","Barcode2","Quantity2","rPrice2", "wPrice2") ,
("Name3","Barcode3","Quantity3","rPrice3", "wPrice3") ,
("Name4","Barcode4","Quantity4","rPrice4", "wPrice4") ,
("Name5","Barcode5","Quantity5","rPrice5", "wPrice5") ,
("Name6","Barcode6","Quantity6","rPrice6", "wPrice6") ,
("Name7","Barcode7","Quantity7","rPrice7", "wPrice7") ,
("Name8","Barcode8","Quantity8","rPrice8", "wPrice8") ,
("Name9","Barcode9","Quantity9","rPrice9", "wPrice9") ,
("Name10","Barcode10","Quantity10","rPrice10", "wPrice10")
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
        self.up_frame = None
        self.tree = None
        self.text = None
        self.scroll = None
        self.up_butt = None
        self.cur = None
        self.modifying = None
        self.n_str = StringVar(self)
        self.b_str = StringVar(self)
        self.q_str = StringVar(self)
        self.rp_str = StringVar(self)
        self.wp_str = StringVar(self)

        # Initialize window components
        self.init_components()

        col, row = self.grid_size()
        for c in range(col):
            self.grid_columnconfigure(c, minsize=25)
        for r in range(row):
            self.grid_rowconfigure(r, minsize=20)
        # Add Label and Button to EDIT window
        # mod_label = Label(self, text="Which database Would you like to view?")
        # mod_label.grid(row=0)
        # out = Label(edit, text=output).grid(row=1)
        # inv_butt = Button(self, text="Inventory", command=lambda: inv())
        # inv_butt.grid(row=1)
        # stat_butt = Button(self, text="Statistics", command=lambda: stat())
        # stat_butt.grid(row=2)
        # bcode_butt = Button(self, text="Barcodes", command=lambda: barcode())
        # bcode_butt.grid(row=3)
        # back_butt = Button(self, text="Go Back", command=self.close_win)
        # back_butt.grid(row=4)

    def init_components(self):
        def hide_widgets():
            n_lbl.grid_remove()
            b_lbl.grid_remove()
            q_lbl.grid_remove()
            rp_lbl.grid_remove()
            wp_lbl.grid_remove()
            n_entry.grid_remove()
            b_entry.grid_remove()
            q_entry.grid_remove()
            rp_entry.grid_remove()
            wp_entry.grid_remove()
            self.up_butt.grid_remove()

        def show_widgets():
            n_lbl.grid()
            b_lbl.grid()
            q_lbl.grid()
            rp_lbl.grid()
            wp_lbl.grid()
            n_entry.grid()
            b_entry.grid()
            q_entry.grid()
            rp_entry.grid()
            wp_entry.grid()
            self.up_butt.grid()

        def mod_clicked():
            if self.cur:
                i = self.tree.item(self.cur)
                self.n_str.set(i["values"][0])
                self.b_str.set(i["values"][1])
                self.q_str.set(i["values"][2])
                self.rp_str.set(i["values"][3])
                self.wp_str.set(i["values"][4])
                self.modifying = True
                show_widgets()

        def select_changed(event):
            if self.modifying:
                if tk.messagebox.askyesno(title="Switch",
                        message="Are you sure you want to terminate modifications?"):
                    self.cur = self.tree.focus()
                    self.n_str.set("")
                    self.b_str.set("")
                    self.q_str.set("")
                    self.rp_str.set("")
                    self.wp_str.set("")
                    self.modifying = False
                    hide_widgets()
            else:
                self.cur = self.tree.focus()

        # Create db_list outer frame
        self.main_frame = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(column=1, row=0, columnspan=5, rowspan=16, sticky=W, padx=25, pady=10)

        # Create frame for updating an entry
        self.up_frame = Frame(self, bg="#d0fbff")
        self.up_frame.grid_rowconfigure(0, weight=1)
        self.up_frame.grid_columnconfigure(0, weight=1)
        self.up_frame.grid(column=7, row=1, columnspan=5, rowspan=14, sticky=W, padx=25, pady=10)

        # Create 5 labels for up_frame
        n_lbl = Label(self.up_frame, text="Name >", font=("Helvetica", 11), bg="#d0fbff")
        n_lbl.grid(row=2, column=7, sticky=E)
        b_lbl = Label(self.up_frame, text="Barcode >", font=("Helvetica", 11), bg="#d0fbff")
        b_lbl.grid(row=5, column=7, sticky=E)
        q_lbl = Label(self.up_frame, text="Quantity >", font=("Helvetica", 11), bg="#d0fbff")
        q_lbl.grid(row=8, column=7, sticky=E)
        rp_lbl = Label(self.up_frame, text="Retail Price >", font=("Helvetica", 11), bg="#d0fbff")
        rp_lbl.grid(row=11, column=7, sticky=E)
        wp_lbl = Label(self.up_frame, text="Wholesale Price >", font=("Helvetica", 11), bg="#d0fbff")
        wp_lbl.grid(row=14, column=7, sticky=E)

        # Create 5 Entry boxes for up_frame
        n_entry = Entry(self.up_frame, textvariable=self.n_str)
        n_entry.grid(row=2, column=8, columnspan=4, pady=15)
        b_entry = Entry(self.up_frame, textvariable=self.b_str)
        b_entry.grid(row=5, column=8, columnspan=4, pady=15)
        q_entry = Entry(self.up_frame, textvariable=self.q_str)
        q_entry.grid(row=8, column=8, columnspan=4, pady=15)
        rp_entry = Entry(self.up_frame, textvariable=self.rp_str)
        rp_entry.grid(row=11, column=8, columnspan=4, pady=15)
        wp_entry = Entry(self.up_frame, textvariable=self.wp_str)
        wp_entry.grid(row=14, column=8, columnspan=4, pady=15)

        # Adding traces to StringVars
        self.n_str.trace("w", self.ok_to_add)
        self.b_str.trace("w", self.ok_to_add)
        self.q_str.trace("w", self.ok_to_add)
        self.rp_str.trace("w", self.ok_to_add)
        self.wp_str.trace("w", self.ok_to_add)

        # Create text area for db entries
        self.tree = ttk.Treeview(self.main_frame, columns=head, show="headings",
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
        self.tree.grid(row=0, column=2, columnspan=3, sticky="nsew", pady=2, padx=2)
        # Binding a selection change to function
        self.tree.bind("<<TreeviewSelect>>", select_changed)

        data = get_dat(Inventory)
        # Populating with database data
        for d in data:
            l = (d["name"], d["barcode"], str(d["quantity"]), "$" + "{:.2f}".format(d["r_price"]),
                 "$" + "{:.2f}".format(d["w_price"]))
            self.tree.insert("", END, values=l)

        # Create scrollbar on right side
        self.scroll = Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scroll.grid(row=0, column=5, rowspan=16, sticky="nse")
        self.tree.config(yscrollcommand=self.scroll.set)

        # Create and place 'Remove' and 'Modify' buttons
        rem_butt = Button(self, text="Remove Selected Item")
        rem_butt.grid(row=17, column=1, rowspan=2, columnspan=2, sticky=W)

        mod_butt = Button(self, text="Modify Selected Item", command=mod_clicked)
        mod_butt.grid(row=17, column=4, rowspan=2, columnspan=2, sticky=W)

        # Create Update Item button
        self.up_butt = Button(self, text="Update Item", state="disabled", command=self.db_update)
        self.up_butt.grid(row=17, column=7, rowspan=2, columnspan=2, sticky=W)

        back_butt = Button(self, text="Go Back", command=self.close_win)
        back_butt.grid(row=17, column=10, rowspan=2, columnspan=2, padx=20)

        # Here we hide the modification widgets
        hide_widgets()

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
        # Here we have a valid item to get added

    def ok_to_add(self, var, index, mode):
        if self.n_str.get() and self.b_str.get() and self.q_str.get() and self.rp_str.get() and self.wp_str.get():
            self.up_butt.config(state="normal")
        else:
            self.up_butt.config(state="disabled")

    def close_win(self):
        self.main_window.deiconify()
        self.destroy()


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


