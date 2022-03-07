# !!NOTE: FOR TESTING PURPOSES AND THIS EARLY VERSION, ALL INPUT OUTPUT WILL BE DONE IN CONSOLE.
# !!THIS SHOULD BE TRANSFERRED TO UI ONCE WE BEGIN TO IMPLEMENT IT.


# DB stores data in the format name: string, barcode: string, quantity: int, price: float

import pymongo
import numpy
import pandas


client = pymongo.MongoClient('mongodb+srv://pygroup:rcagroup@cluster0.uxruw.mongodb.net/Cluster0?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority')
db = client["InvManager"]
collection = db["Inventory"]


def getDat():
    dicts = []
    for x in collection.find():
        dicts.append(x)

    return dicts


def setDat():
    # Functionally basic set statement, that ensures that product names and barcodes are unique.
    # Plan on implementing more in depth additive quantities or something similar later and
    # potentially more data.
    name = input("Insert name: ")
    x = collection.find({"name": name})
    if len(list(x)) > 0:
        found = input("An item with this name exists. Would you like to modify it? (y/n):").lower()
        if found == "y":
            bcode = input("Insert barcode number: ")
            quan = input("Insert quantity: ")
            price = input("Insert price: ")
            return collection.update_one({"name": name}, {"$set": {"name": name, "barcode": bcode,
                                                                   "quantity": int(quan), "price": float(price)}})
    bcode = input("Insert barcode number: ")
    y = collection.find({"barcode": bcode})
    if len(list(y)) > 0:
        found = input("An item with this name exists. Would you like to modify it? (y/n):").lower()
        if found == "y":
            quan = input("Insert quantity: ")
            price = input("Insert price: ")
            return collection.update_one({"barcode": bcode}, {"$set": {"name": name, "barcode": bcode,
                                                                       "quantity": int(quan), "price": float(price)}})
    quan = input("Insert quantity: ")
    price = input("Insert price: ")
    return collection.insert_one({"name": name, "barcode": bcode, "quantity": int(quan), "price": float(price)})


def editDat():
    # NOT IMPLEMENTED
    return 0


def delDat():
    name_bar = input("Insert name/barcode of item to be removed:")
    return collection.delete_one({"$or": [{"name": name_bar}, {"barcode": name_bar}]})

# !! SORT NOT WORKING, UNSURE AS TO WHY
def sortDat():
    print("What would you like to sort by?")
    sort = input("(N)ame, (B)arcode, (Q)uantity, (P)rice:").lower()
    asOdes = input("(A)scending or (D)escending order:").lower()

    if sort == "n":
        if asOdes == "a":
            return collection.find().sort("name")
        elif asOdes == "d":
            return collection.find().sort("name", -1)
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "b":
        if asOdes == "a":
            return collection.find().sort("barcode")
        elif asOdes == "d":
            return collection.find().sort("barcode", -1)
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "q":
        if asOdes == "a":
            return collection.find().sort("quantity")
        elif asOdes == "d":
            return collection.find().sort("quantity", -1)
        else:
            print("Error: invalid input for Ascending/Descending.")
    elif sort == "p":
        if asOdes == "a":
            return collection.find().sort("price")
        elif asOdes == "d":
            return collection.find().sort("price", -1)
        else:
            print("Error: invalid input for Ascending/Descending.")
    else:
        print("Error: invalid input for sort type.")

    return


def getStats():
    # NOT IMPLEMENTED
    return 0


if __name__ == '__main__':
    loop = True
    print("Welcome to INVENTORY MANAGER testing.")
    while loop is True:
        print("What would you like to do?")
        print("P: Print data")
        print("A: Add data")
        print("R: Remove data")
        print("S: Sort data")
        print("X: Exit")
        inp = input().lower()
        if inp == "p":
            result = getDat()
            j = 0
            for i in result:
                j += 1
                print("[" + str(j) + "]")
                print("Name: " + i['name'] + ", Barcode: " + i['barcode'] + ", Quantity: " + str(i['quantity'])
                      + ", Price: $" + str(i['price']))
        elif inp == "a":
            result = setDat()

        elif inp == "r":
            result = delDat()

        elif inp == "s":
            result = sortDat()

        elif inp == "x":
            loop = False
        else:
            print(inp + " = Invalid input. Try again.")