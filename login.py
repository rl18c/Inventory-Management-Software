import pymongo
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
client = pymongo.MongoClient("localhost:27017")

db = client["loginManager"]
login = db["logins"]
Inventory = ""
NameBcode = ""
Stats = ""

class UI(tk.Tk):

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
            Inventory = db["newuser"]
            self.top.destroy()
            self.withdraw()
            loginm = loginMessage(self)
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
                    loguser = db[self.newusertxt.get()]
                    loguser.insert_one({"price" : 69})
                    print(db.list_collection_names())
                    self.top.destroy()
                    self.withdraw()
                    loginm = loginMessage(self)
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
            self.top.destroy()
        else:
            self.deleteusertxt.delete(0, END)
            self.deletepasstxt.delete(0, END)
            tkinter.messagebox.showinfo("Error", "Error: Account not Found")
            self.top.lift()

class loginMessage(tk.Tk):
    def __init__(self, mas):
        super().__init__()
        self.main_window = mas
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
        title_label = Label(self, text="Logged In",
                            bg="#d0fbff",
                            fg="#9e5f00",
                            font=("Helvetica", 16))
        title_label.grid(row=0, column=1, columnspan=3, sticky=EW, pady=10)

        but1_border = Frame(self, highlightthickness=2, highlightbackground="#37d3ff")
        but1_border.grid(column=0, row=1, columnspan=2, sticky=W, padx=25, pady=10)

        delete_butt = Button(but1_border, text="Log Out",
                          bg="white",
                          borderwidth=0,
                          font=("Helvetica", 11),
                          command=self.logOut)
        delete_butt.grid()
        delete_butt.config(width=18)
        self.protocol("WM_DELETE_WINDOW", self.closingPop)

    def logOut(self):
        self.main_window.deiconify()
        self.destroy()
    def closingPop(self):
        self.main_window.deiconify()
        self.destroy()

if __name__ == '__main__':
    window = UI()
    window.mainloop()



"""
while True:
    menu()
    option = input()
    if(int(option) == 1):
        user = input()
        password = input()
        if login.find_one({"name" : user, "password" : password}):
            #grab correct inv
            print("succ")
        else:
            print("notfound")
    elif(int(option) == 2):
        user = input()
        password = input()
        if login.find_one({"name" : user, "password" : password}):
            print("exists")
        else:
            login.insert_one({"name" : user, "password" : password})
            loguser = db[user]
            loguser.insert_one({"price" : 69})
            print(db.list_collection_names())
    elif(int(option) == 3):
        user = input()
        password = input()
        if login.find_one({"name" : user, "password" : password}):
            login.delete_one({"name" : user, "password" : password})
        else:
            print("not found")
    else:
        break
"""
