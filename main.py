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
import pandas
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import tkinter as tk
from tkinter import *
import tkcalendar as cal
from collections import OrderedDict
import os
import tkinter.messagebox

client = pymongo.MongoClient("mongodb+srv://pygroup:rcagroup@project.uxruw.mongodb.net/InvManager")


db = client["InvManager"]
loginsdb = client["loginManager"]
login = loginsdb["logins"]
Inventory = ""
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


class Login(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("500x220")
        self.title("Inventory Manager")
        self.resizable(False, False)
        self.configure(bg="#d0fbff")

        self.initialize_components()

        col, row = self.grid_size()
        for c in range(col):
            self.grid_columnconfigure(c, minsize=100)

    def initialize_components(self):
        # Title Label
        title_label = Label(self, text="Inventory Manager",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        title_label.grid(row=0, column=1, columnspan=3, sticky=EW, pady=10)

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
        but4_border.grid(column=2, row=3, columnspan=2, padx=25)

        # login button
        login_butt = Button(but1_border, text="Login",
                          bg="white",
                          borderwidth=0,
                          font=("Helvetica", 11),
                          command=self.login)
        login_butt.grid()
        login_butt.config(width=18)

        # signup button
        signup_butt = Button(but2_border, text="Sign Up",
                           bg="white",
                           font=("Helvetica", 11),
                           borderwidth=0,
                           command=self.signUp)
        signup_butt.grid()
        signup_butt.config(width=18)

        # delete account button
        delete_butt = Button(but3_border, text="Delete Account",
                           bg="white",
                           font=("Helvetica", 11),
                           borderwidth=0,
                           command=self.delete)
        delete_butt.grid()
        delete_butt.config(width=18)

        # Close Window Button
        close_butt = Button(but4_border, text="Close Manager",
                            bg="white",
                            font=("Helvetica", 11),
                            borderwidth=0,
                            command=self.destroy)
        close_butt.grid()
        close_butt.config(width=18)

    def login(self):
        self.top = Toplevel(self)
        self.top.geometry("300x150")
        self.top.title("login info")
        self.top.configure(bg="#d0fbff")

        user_label=Label(self.top, text="Username",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        user_label.grid(row=0, column=0, columnspan=1, sticky=EW, pady=10)

        pass_label=Label(self.top, text="Password",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        pass_label.grid(row=1, column=0, columnspan=1, sticky=EW, pady=10)

        self.usertxt = Entry(self.top)
        self.usertxt.grid(row=0, column=1, columnspan=3, sticky=EW, pady=10)

        self.passtxt = Entry(self.top)
        self.passtxt.config(show="*")
        self.passtxt.grid(row=1, column=1, columnspan=3, sticky=EW, pady=10)

        enter_butt = Button(self.top, text="Enter",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.loginCheck)
        enter_butt.grid(row=3, column=0, columnspan=2, sticky=EW, pady=10, padx=22)
        enter_butt.config(width=12, height=1)

        cancel_butt = Button(self.top, text="Cancel",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.top.destroy)
        cancel_butt.grid(row=3, column=2, columnspan=2, sticky=EW, pady=10)
        cancel_butt.config(width=12, height=1)

    def loginCheck(self):
        if login.find_one({"name" : self.usertxt.get(), "password" : self.passtxt.get()}):
            #grab correct inv
            global Inventory
            global Stats
            global NameBcode
            Stats = db[self.usertxt.get() + "-Stats"]
            Inventory = db[self.usertxt.get() + "-Inventory"]
            NameBcode = db[self.usertxt.get() + "-NameBarcode"]
            self.top.destroy()
            self.withdraw()
            loginm = UI(self)
        else:
            self.usertxt.delete(0, END)
            self.passtxt.delete(0, END)
            tkinter.messagebox.showinfo("Error", "Error: Username or Password Incorrect")
            self.top.lift()

    def signUp(self):
        self.top = Toplevel(self)
        self.top.geometry("400x200")
        self.top.title("sign-up")
        self.top.configure(bg="#d0fbff")

        user_label=Label(self.top, text="Enter Username",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        user_label.grid(row=0, column=0, columnspan=1, sticky=EW, pady=10)

        pass_label=Label(self.top, text="Enter Password",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        pass_label.grid(row=1, column=0, columnspan=1, sticky=EW, pady=10)

        pass_label=Label(self.top, text="Re-Enter Password",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        pass_label.grid(row=2, column=0, columnspan=1, sticky=EW, pady=10)

        self.newusertxt = Entry(self.top)
        self.newusertxt.grid(row=0, column=1, columnspan=5, sticky=EW, pady=10)

        self.newpasstxt = Entry(self.top)
        self.newpasstxt.config(show="*")
        self.newpasstxt.grid(row=1, column=1, columnspan=5, sticky=EW, pady=10)

        self.newpass2txt = Entry(self.top)
        self.newpass2txt.config(show="*")
        self.newpass2txt.grid(row=2, column=1, columnspan=5, sticky=EW, pady=10)

        enter_butt = Button(self.top, text="Enter",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.signUpCheck)
        enter_butt.grid(row=3, column=0, columnspan=2, sticky=EW, pady=10, padx=22)
        enter_butt.config(width=12, height=1)

        cancel_butt = Button(self.top, text="Cancel",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.top.destroy)
        cancel_butt.grid(row=3, column=2, columnspan=2, sticky=EW, pady=10)
        cancel_butt.config(width=12, height=1)

    def signUpCheck(self):
        if(self.newusertxt.get() == "" or self.newpasstxt == ""):
            self.newusertxt.delete(0, END)
            self.newpasstxt.delete(0, END)
            self.newpass2txt.delete(0, END)
            tkinter.messagebox.showinfo("Error", "Error: Username or Password can not be Blank")
            self.top.lift()
        else:
            if(self.newpass2txt.get() == self.newpasstxt.get()):
                if login.find_one({"name" : self.newusertxt.get(), "password" : self.newpasstxt.get()}):
                    self.newusertxt.delete(0, END)
                    self.newpasstxt.delete(0, END)
                    self.newpass2txt.delete(0, END)
                    tkinter.messagebox.showinfo("Error", "Error: Username Already Exists")
                    self.top.lift()
                else:
                    login.insert_one({"name" : self.newusertxt.get(), "password" : self.newpasstxt.get()})

                    Inventory = db[self.newusertxt.get() + "-Inventory"]
                    Stats = db[self.newusertxt.get() + "-Stats"]
                    NameBcode = db[self.newusertxt.get() + "-NameBarcode"]
                    #Inventory.insert_one({"r_price" : 0, "w_price" : 0, "name" : "Test-Stub", "quantity" : 0, "barcode" : 0})
                    self.top.destroy()
                    self.withdraw()
                    loginm = UI(self)
            else:
                self.newpasstxt.delete(0, END)
                self.newpass2txt.delete(0, END)
                tkinter.messagebox.showinfo("Error", "Error: Password Mismatch")
                self.top.lift()

    def delete(self):
        self.top = Toplevel(self)
        self.top.geometry("300x150")
        self.top.title("Delete Account")
        self.top.configure(bg="#d0fbff")

        user_label=Label(self.top, text="Username",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        user_label.grid(row=0, column=0, columnspan=1, sticky=EW, pady=10)

        pass_label=Label(self.top, text="Password",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        pass_label.grid(row=1, column=0, columnspan=1, sticky=EW, pady=10)

        self.deleteusertxt = Entry(self.top)
        self.deleteusertxt.grid(row=0, column=1, columnspan=3, sticky=EW, pady=10)

        self.deletepasstxt = Entry(self.top)
        self.deletepasstxt.config(show="*")
        self.deletepasstxt.grid(row=1, column=1, columnspan=3, sticky=EW, pady=10)

        enter_butt = Button(self.top, text="Enter",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.deleteCheck)
        enter_butt.grid(row=3, column=0, columnspan=2, sticky=EW, pady=10, padx=22)
        enter_butt.config(width=12, height=1)

        cancel_butt = Button(self.top, text="Cancel",
                          bg="white",
                          borderwidth=1,
                          font=("Helvetica", 11),
                          command=self.top.destroy)
        cancel_butt.grid(row=3, column=2, columnspan=2, sticky=EW, pady=10)
        cancel_butt.config(width=12, height=1)

    def deleteCheck(self):
        if login.find_one({"name" : self.deleteusertxt.get(), "password" : self.deletepasstxt.get()}):
            login.delete_one({"name" : self.deleteusertxt.get(), "password" : self.deletepasstxt.get()})
            Inventory.drop()
            self.top.destroy()
        else:
            self.deleteusertxt.delete(0, END)
            self.deletepasstxt.delete(0, END)
            tkinter.messagebox.showinfo("Error", "Error: Account not Found")
            self.top.lift()

class UI(tk.Tk):
    def __init__(self, mas):
        super().__init__()
        # self.geometry("500x220")
        self.main_window = mas
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
        self.expt_butt = None
        self.imp_butt = None
        self.exp_butt = None
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
        #Export button border
        exp_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        exp_bord.grid(column=11, row=20, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)

        # Export Template button border
        expt_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        expt_bord.grid(column=11, row=17, columnspan=2, rowspan=2, sticky=W, padx=25)
        # Import button border
        imp_bord = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        imp_bord.grid(column=11, row=14, columnspan=2, rowspan=2, sticky=W, padx=25, pady=10)
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

        # Export Data Button
        self.exp_butt = Button(exp_bord, text="Export Data",
                               bg="white",
                               borderwidth=0,
                               font=("Helvetica", 11),
                               command=self.inv_exp)
        self.exp_butt.grid()
        self.exp_butt.config(width=18)

        # Export Template Data Button
        self.expt_butt = Button(expt_bord, text="Create Import Template",
                               bg="white",
                               borderwidth=0,
                               font=("Helvetica", 11),
                               command=self.inv_expt)
        self.expt_butt.grid()
        self.expt_butt.config(width=18)

        # Import Data Button
        self.imp_butt = Button(imp_bord, text="Import Data",
                               bg="white",
                               borderwidth=0,
                               font=("Helvetica", 11),
                               command=self.inv_imp)
        self.imp_butt.grid()
        self.imp_butt.config(width=18)

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

    def inv_exp(self):
        # Hides Original window while modifying
        #self.withdraw()
        # This is where we must open new window to add Inventory DB
        #expd = ExportData(self)
        directory = tk.filedialog.askdirectory(initialdir="/", title='Please select a directory for Export')
        if directory:
            filename = None
            popup = tk.Tk()
            popup.wm_title("Input name for file")
            popup.eval('tk::PlaceWindow . center')
            label = ttk.Label(popup, text="Input a name for your spreadsheet")
            label.pack(side="top", fill="x", pady=10)
            n_entry = Entry(popup, textvariable=filename)
            n_entry.pack()
            def get_in():
                nonlocal filename
                nonlocal directory
                filename = n_entry.get()
                if filename:
                    popup.destroy()
                path = directory +"/"+ filename + ".xlsx"
                if os.path.exists(path):
                    MsgBox = tk.messagebox.askquestion('File Exists',
                                                       'File exists. Would you like to overwrite the file?',
                                                       icon='warning')
                    if MsgBox == 'yes':
                        try:
                            os.remove(path)
                        except:
                            tk.messagebox.showerror('Error', 'Error replacing file: File in use.')
                            return
                    else:
                        return
                d1 = pandas.DataFrame.from_dict(get_dat(Inventory))
                d1 = d1.iloc[:, 1:]
                d2 = pandas.DataFrame.from_dict(get_dat(Stats))
                d2 = d2.iloc[:, 1:]
                d2['time'] = d2['time'].astype(str)
                d3 = pandas.DataFrame.from_dict(get_dat(NameBcode))
                d3 = d3.iloc[:, 1:]
                writer = pandas.ExcelWriter(path, engine='xlsxwriter')

                d1.to_excel(writer, sheet_name='Inventory')
                d2.to_excel(writer, sheet_name='Statistics')
                d3.to_excel(writer, sheet_name='Unique Name Barcodes')
                writer.save()
                if os.path.exists(path):
                    tk.messagebox.showinfo('Success!', 'File created successfully.')
                else:
                    tk.messagebox.showerror('Error', 'Error creating file.')



            B1 = ttk.Button(popup, text="Submit", command=get_in)
            B1.pack()

    def inv_expt(self):
        # Hides Original window while modifying
        #self.withdraw()
        # This is where we must open new window to add Inventory DB
        #expd = ExportData(self)
        directory = tk.filedialog.askdirectory(initialdir="/", title='Please select a directory for Export')
        if directory:
            path = directory +"/template.xlsx"
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    tk.messagebox.showerror('Error', 'Error remaking file: template.xlsx in use.')
                    return
                inv_data= [['NAME', '0000', 0, "0.00", "0.00"]]
                stat_data = [['YEAR-MO-DA HO:MI:SE.MIS', '0000', 0, "0.00", "0.00"]]
                nbc_data = [['NAME', '0000']]
                d1 = pandas.DataFrame(inv_data, columns=['name', 'barcode', 'quantity', 'r_price', 'w_price'])
                d2 = pandas.DataFrame(stat_data, columns=['time', 'barcode', 'quantity', 'r_price', 'w_price'])
                d3 = pandas.DataFrame(nbc_data, columns=['name', 'barcode'])
                writer = pandas.ExcelWriter(path, engine='xlsxwriter')

                d1.to_excel(writer, sheet_name='Inventory')
                d2.to_excel(writer, sheet_name='Statistics')
                d3.to_excel(writer, sheet_name='Unique Name Barcodes')
                writer.save()
            else:
                inv_data = [['NAME', '0000', 0, "0.00", "0.00"]]
                stat_data = [['YEAR-MO-DA HO:MI:SE.MIS', '0000', 0, "0.00", "0.00"]]
                nbc_data = [['NAME', '0000']]
                d1 = pandas.DataFrame(inv_data, columns=['name', 'barcode', 'quantity', 'r_price', 'w_price'])
                d2 = pandas.DataFrame(stat_data, columns=['time', 'barcode', 'quantity', 'r_price', 'w_price'])
                d3 = pandas.DataFrame(nbc_data, columns=['name', 'barcode'])
                writer = pandas.ExcelWriter(path, engine='xlsxwriter')

                d1.to_excel(writer, sheet_name='Inventory')
                d2.to_excel(writer, sheet_name='Statistics')
                d3.to_excel(writer, sheet_name='Unique Name Barcodes')
                writer.save()
            if os.path.exists(path):
                tk.messagebox.showinfo('Success!', 'File created successfully.')
            else:
                tk.messagebox.showerror('Error', 'Error creating file.')

    def inv_imp(self):
        # Hides Original window while modifying
        # self.withdraw()
        # This is where we must open new window to add Inventory DB
        # expd = ExportData(self)
        file = tk.filedialog.askopenfilename(initialdir="/", title='Please select a file for Import')
        if file == "":
            return
        try:
            xls = pandas.ExcelFile(file)
        except:
            tk.messagebox.showerror('Error', 'Error opening file: Not an excel file.')
            return
        d1 = xls.parse(xls.sheet_names[0])  # Inventory
        d2 = xls.parse(xls.sheet_names[1])  # Stats
        d3 = xls.parse(xls.sheet_names[2])  # NameBcode
        # except:
        #   tk.messagebox.showerror('Error', 'Error opening file.')
        #  return
        if file:
            result = tk.messagebox.askyesnocancel("Data Replacement",
                                                  "Would you like to replace the database? (select no for append)\n"
                                                  "(Note: Make sure the file is formatted like the export file)")
            # Above is temporary until i can make my own message box
            if result is True:
                d1 = d1.reset_index()
                d2 = d2.reset_index()
                d3 = d3.reset_index()
                for index, row in d1.iterrows():
                    try:
                        n = row["name"]
                        b = row["barcode"]
                        q = int(row["quantity"])
                        r = float(row["r_price"])
                        w = float(row["w_price"])
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Inventory sheet formatted improperly.')
                        return
                for index, row in d2.iterrows():
                    try:
                        t = datetime.strptime(row["time"], '%Y-%m-%d %H:%M:%S.%f')
                        b = row["barcode"]
                        q = int(row["quantity"])
                        r = float(row["r_price"])
                        w = float(row["w_price"])
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Statistics sheet formatted improperly.')
                        return
                for index, row in d3.iterrows():
                    try:
                        n = row["name"]
                        b = row["barcode"]
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Unique Name Barcodes sheet formatted improperly.')
                        return

                Inventory.delete_many({})
                Stats.delete_many({})
                NameBcode.delete_many({})
                d1 = d1.reset_index()
                d2 = d2.reset_index()
                d3 = d3.reset_index()
                for index, row in d1.iterrows():
                    try:
                        Inventory.insert_one({"name": row["name"], "barcode": row["barcode"],
                                              "quantity": int(row["quantity"]), "r_price": float(row["r_price"]),
                                              "w_price": float(row["w_price"])})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Inventory sheet formatted improperly.')
                        return
                for index, row in d2.iterrows():
                    dt_obj = datetime.strptime(row["time"], '%Y-%m-%d %H:%M:%S.%f')
                    try:
                        Stats.insert_one({"time": dt_obj, "barcode": row["barcode"], "quantity": int(row["quantity"]),
                                          "r_price": float(row["r_price"]), "w_price": float(row["w_price"])})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Statistics sheet formatted improperly.')
                        return
                for index, row in d3.iterrows():
                    try:
                        NameBcode.insert_one({"name": row["name"], "barcode": row["barcode"]})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Unique Name Barcodes sheet formatted improperly.')
                        return
                tk.messagebox.showinfo('Success!', 'Database written successfully.')


            elif result is False:
                d1 = d1.reset_index()
                d2 = d2.reset_index()
                d3 = d3.reset_index()
                for index, row in d1.iterrows():
                    try:
                        n = row["name"]
                        b = row["barcode"]
                        q = int(row["quantity"])
                        r = float(row["r_price"])
                        w = float(row["w_price"])
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Inventory sheet formatted improperly.')
                        return
                for index, row in d2.iterrows():
                    try:
                        t = datetime.strptime(row["time"], '%Y-%m-%d %H:%M:%S.%f')
                        b = row["barcode"]
                        q = int(row["quantity"])
                        r = float(row["r_price"])
                        w = float(row["w_price"])
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Statistics sheet formatted improperly.')
                        return
                for index, row in d3.iterrows():
                    try:
                        n = row["name"]
                        b = row["barcode"]
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Unique Name Barcodes sheet formatted improperly.')
                        return
                d1 = d1.reset_index()
                d2 = d2.reset_index()
                d3 = d3.reset_index()
                for index, row in d3:
                    name = NameBcode.find_one({"name": row["name"]})
                    code = NameBcode.find_one({"barcode": row["barcode"]})
                    if name or code:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Unique barcode' + row["name"] + ': '
                                                + row["barcode"] + ' already used.')
                        return

                for index, row in d2.iterrows():
                    try:
                        dt_obj = datetime.strptime(row["time"], '%Y-%m-%d %H:%M:%S.%f')
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: Times formatted improperly.')
                        return
                    try:
                        Stats.insert_one({"time": dt_obj, "barcode": row["barcode"], "quantity": int(row["quantity"]),
                                          "r_price": float(row["r_price"]), "w_price": float(row["w_price"])})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Statistics sheet formatted improperly.')
                        return
                for index, row in d3.iterrows():
                    try:
                        NameBcode.insert_one({"name": row["name"], "barcode": row["barcode"]})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Unique Name Barcodes sheet formatted improperly.')
                        return
                for index, row in d1.iterrows():
                    try:
                        Inventory.insert_one({"name": row["name"], "barcode": row["barcode"],
                                              "quantity": int(row["quantity"]), "r_price": float(row["r_price"]),
                                              "w_price": float(row["w_price"])})
                        if not Stats.find_one({"barcode": row["barcode"]}):
                            Stats.insert_one({"time": datetime.now(), "barcode": row["barcode"],
                                              "quantity": int(row["quantity"]), "r_price": float(row["r_price"]),
                                              "w_price": float(row["w_price"])})
                        if not NameBcode.find_one(row["barcode"]) or not NameBcode.find_one(row["name"]):
                            NameBcode.insert_one({"name": row["name"], "barcode": row["barcode"]})
                    except:
                        tk.messagebox.showerror('Error', 'Error converting file: '
                                                         'Inventory sheet formatted improperly.')
                        return

                tk.messagebox.showinfo('Success!', 'Database written successfully.')

            elif result is None:
                print("cancel")
                return

    def close_main(self):
        self.destroy()
        exit()


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
        self.withdraw()
        if self.sel_barcode is None:
            self.calender_select(1, 0)
        else:
            self.calender_select(0, 0)

    def prof_options(self):
        self.withdraw()
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
                item = NameBcode.find_one({"barcode": float(code)})
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
                item = NameBcode.find_one({"barcode": float(code)})
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

                tree_prof_frame = Frame(self.popup_g, highlightthickness=2,
                                        highlightbackground="#37d3ff")
                tree_prof_frame.grid(row=3, column=8, columnspan=4, rowspan=15, sticky=EW)
                tree_prof = ttk.Treeview(tree_prof_frame, columns=["Name", "Profit"], show="headings",
                                         height=15)
                tree_prof.grid_rowconfigure(0, weight=1)
                tree_prof.grid_columnconfigure(0, weight=1)

                # Define each column's width
                tree_prof.column("Name", anchor=CENTER, width=80)
                tree_prof.column("Profit", anchor=CENTER, width=80)

                # Define heading's text
                tree_prof.heading("Name", text="Name")
                tree_prof.heading("Profit", text="Profit")
                tree_prof.grid(row=3, column=8, rowspan=15, columnspan=3, sticky="nsew", pady=5, padx=5)

                for key, value in sorted_p.items():
                    v = "{:.2f}".format(value)
                    l = (key, v)
                    tree_prof.insert("", END, values=l)

                scroll_prof = Scrollbar(tree_prof_frame, orient="vertical", command=tree_prof.yview)
                scroll_prof.grid(row=3, column=11, rowspan=15, sticky="nse")
                tree_prof.config(yscrollcommand=scroll_prof.set)

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
        b1 = Button(close_bord, text="Return to Graph Selection",
                    command=self.close_graph,
                    bg="white",
                    font=("Helvetica", 10),
                    borderwidth=0)
        b1.grid()
        self.popup_g.mainloop()

    def close_win(self):
        self.main_window.deiconify()
        self.destroy()

    def close_graph(self):
        self.deiconify()
        self.popup_g.destroy()


if __name__ == '__main__':
    window = Login()
    window.mainloop()
