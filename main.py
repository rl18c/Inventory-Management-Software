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


if __name__ == '__main__':
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
