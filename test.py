from LocalStorage import LocalStorage

if __name__ == "__main__":
    localstore = LocalStorage()
    localstore.create("MGHector", {"type": "Mid Size Suv", "capacity": 5})
    localstore.create("MGHectorPlus", {"type": "Mid Size Suv", "capacity": 7})

    print(localstore.get("MGHector"))

    try:
        localstore.create("Seltos", "Car Model")
    except Exception as e:
        print("Exception occurred: ", e)

    try:
        localstore.create("ThisIsaKeyWithLengthMoreThan32Characters", {"type": "Mid Size Suv", "capacity": 5})
    except Exception as e:
        print("Exception occurred: ", e)

    try:
        localstore.create("MGHector", {"type": "Mid Size Suv", "capacity": 6})
    except Exception as e:
        print("Exception occurred: ", e)

    try:
        localstore.get("NonExistingKey")
    except Exception as e:
        print("Exception occurred: ", e)

    #Delete file
    print(localstore.get("MGHectorPlus"))
    localstore.delete("MGHectorPlus")
    try:
        localstore.get("MGHectorPlus")
    except Exception as e:
        print("Exception occurred: ", e)
