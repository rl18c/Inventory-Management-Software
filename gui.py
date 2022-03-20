import tkinter as tk
from tkinter import *

class Inventory(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x600")
        self.title("Inventory Manager")
        self.resizable(0,0)
        
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.initialize_components()


    def initialize_components(self):
        #Title Label
        title_label = Label(self, text="Choose Option")
        title_label.grid(columnspan=2)
        
        #Edit Data Button
        edit_butt = Button(self, text="Add/Edit Inventory", command=self.inv_edit)
        edit_butt.grid(column=0,row=1)
        
        #Close Window Button
        close_butt = Button(self, text="Close Manager", command=self.close_main)
        close_butt.grid(column=1,row=1)
        
    def inv_edit(self):
        print("Accessing Inventory...")
        
        #This is where we must open new window to edit Inventory DB
        edit = Toplevel(self)
        
        edit.title("Data Modification")
        edit.geometry("200x200")
        
        #Add Label and Button to EDIT window
        mod_label = Label(edit, text="Testing the Layers Donkey").grid(row=0)
        back_butt = Button(edit, text="Go Back", command=lambda: self.close_edit(edit))
        back_butt.grid(row=1)
        
        #Hides Original window while modifying
        self.withdraw()
    
    #Function used by EDIT's 'Go Back' button to close current and open original
    def close_edit(self, win):
        win.destroy()
        self.deiconify()
            
    def close_main(self):
        self.destroy()
                
    def greet(self):
        print("Greetings!")


if __name__ == "__main__":
    window = Inventory()
    window.mainloop()