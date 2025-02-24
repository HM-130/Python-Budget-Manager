from summary import summary
from crud import addTransaction, addIncome, addLongTerm, viewTransactions, viewIncome, viewLongTerm, updateTransaction, updateIncome, updateLongTerm, deleteTransaction, deleteIncome, deleteLongTerm, readFile
import datetime

def checkDate(date):
    try:
        datetime.strptime(date, "%d/%m/%Y")
        return True
    except:
        return False

def mainMenu():
    print("\nWelcome to my Personal Budget Manager!")
    main = True
    while main:
        print("\nMain Menu:")
        print("1: Add an income, transaction, or long-term income/expense/goal")
        print("2: Edit an income, transaction, or long-term income/expense/goal")
        print("3: Delete an income, transaction, or long-term income/expense/goal")
        print("4: View a comprehensive financial summary over your chosen time period")
        print("5: Exit")
        userOption = input("Enter your chosen option (1-5): ").strip()
        try:
            userOption = int(userOption)

            if userOption == 1:
                userAddOption = input("Add an income (i), transaction (t), or long-term goal (l)? ").strip().lower()
                if userAddOption == "i":
                    date = input("Enter the date (DD/MM/YYYY): ").strip()
                    amount = float(input("Enter the income amount: £"))
                    if checkDate(date):
                        try:
                            addIncome(date, amount)
                            print("Income added successfully")
                        except:
                            print(f"Error adding income")
                    else:
                        print("Invalid date entry, please re-enter")
                elif userAddOption == "t":
                    category = input("Enter the category: ").strip().title()
                    date = input("Enter the date (DD/MM/YYYY): ").strip()
                    location = input("Enter the location: ").strip().title()
                    amount = float(input("Enter the transaction amount: £"))
                    if checkDate(date):
                        try:
                            addTransaction(category, date, location, amount)
                            print("Transaction added successfully")
                        except:
                            print(f"Error adding transaction")
                    else:
                        print("Invalid date entry, please re-enter")
                elif userAddOption == "l":
                    incomeOrExpenseOrGoal = input("Enter 'Income', 'Expense', or 'Goal': ").strip()
                    timePeriod = input("Enter the time period (Monthly/Yearly): ").strip()
                    amount = float(input("Enter the amount: £"))
                    source = input("Enter the source or date (DD/MM/YYYY) for goal: ").strip()
                    try:
                        addLongTerm(incomeOrExpenseOrGoal, timePeriod, amount, source)
                        print("Long-term line added successfully")
                    except :
                        print(f"Error adding long-term line")
                else:
                    print("Invalid option. Please try again")

            elif userOption == 2:
                userEditOption = input("Edit an income (i), transaction (t), or long-term goal (l)? ").strip().lower()
                
                if userEditOption == "i":
                    idFound = False
                    viewIncome()
                    updateId = input("Enter the ID of the line to update: ").strip()
                    date = input("Enter the new date (DD/MM/YYYY): ").strip()
                    amount = float(input("Enter the new amount: £"))
                    lines = readFile("incomes.csv")
                    for line in lines: 
                        if line.startswith(updateId + ","):
                            idFound = True
                    if idFound:
                        if checkDate(date):
                            try:
                                if updateIncome(updateId, date, amount):
                                    print("Income updated successfully")
                                else:
                                    print("Error: No income line found with that ID")
                            except:
                                print(f"Error updating income")
                        else:
                            print("Invalid date entry, please re-enter")
                    else:
                        print("Update ID not found in incomes.csv, please try again")

                elif userEditOption == "t":
                    idFound = False
                    viewTransactions()
                    updateId = input("Enter the ID of the line to update: ").strip()
                    category = input("Enter the new category: ").strip().title()
                    date = input("Enter the new date (DD/MM/YYYY): ").strip()
                    location = input("Enter the new location: ").strip().title()
                    amount = float(input("Enter the new amount: £"))
                    lines = readFile("transactions.csv")
                    for line in lines: 
                        if line.startswith(updateId + ","):
                            idFound = True
                    if idFound:
                        if checkDate(date):
                            try:
                                if updateTransaction(updateId, category, date, location, amount):
                                    print("Transaction updated successfully")
                                else:
                                    print("Error: No transaction line found with that ID")
                            except:
                                print(f"Error updating transaction")
                        else:
                            print("Invalid date entry, please re-enter")
                    else:
                        print("Update ID not found in transactions.csv, please try again")

                elif userEditOption == "l":
                    idFound = False
                    viewLongTerm()
                    updateId = input("Enter the ID of the line to update: ").strip()
                    incomeOrExpenseOrGoal = input("Enter the new type - 'Income', 'Expense', or 'Goal': ").strip().title()
                    timePeriod = input("Enter the new time period (Monthly/Yearly): ").strip().title()
                    amount = float(input("Enter the new amount: £"))
                    source = input("Enter the new source or starting date (DD/MM/YYYY) for goal: ").strip()
                    lines = readFile("longTerm.csv")
                    for line in lines: 
                        if line.startswith(updateId + ","):
                            idFound = True
                    if idFound:
                        try:
                            if updateLongTerm(updateId, incomeOrExpenseOrGoal, timePeriod, amount, source):
                                print("Long-term line updated successfully")
                            else:
                                print("Error: No long-term line found with that ID")
                        except:
                            print(f"Error updating long-term line")
                    else:
                        print("Update ID not found in longTerm.csv, please try again")
            
            elif userOption == 3:
                userDeleteOption = input("Delete an income (i), transaction (t), or long-term goal (l)? ").strip().lower()
                if userDeleteOption == "i":
                    idFound = False
                    viewIncome()
                    deleteId = input("Enter the ID of the line to delete: ").strip()
                    lines = readFile("incomes.csv")
                    for line in lines:
                        if line.startswith(deleteId + ","):
                            idFound = True
                    if idFound:
                        try:
                            deleteIncome(deleteId)
                            print("Income deleted successfully")
                        except:
                            print(f"Error deleting income")
                    else:
                        print("Delete ID not found in incomes.csv, please try again")
                elif userDeleteOption == "t":
                    idFound = False
                    viewTransactions()
                    deleteId = input("Enter the ID of the line to delete: ").strip()
                    lines = readFile("transactions.csv")
                    for line in lines:
                        if line.startswith(deleteId + ","):
                            idFound = True
                    if idFound:
                        try:
                            deleteTransaction(deleteId)
                            print("Transaction deleted successfully")
                        except:
                            print(f"Error deleting transaction")
                    else:
                        print("Delete ID not found in transactions.csv, please try again")
                elif userDeleteOption == "l":
                    idFound = False
                    viewLongTerm()
                    deleteId = input("Enter the ID of the line to delete: ").strip()
                    lines = readFile("longTerm.csv")
                    for line in lines:
                        if line.startswith(deleteId + ","):
                            idFound = True
                    if idFound:
                        try:
                            deleteLongTerm(deleteId)
                            print("Long-term line deleted successfully")
                        except:
                            print(f"Error deleting long-term line")
                    else:
                        print("Delete ID not found in longTerm.csv, please try again")
                else:
                    print("Invalid option. Please try again")
                
            elif userOption == 4:
                userDays = input("Enter the number of days for the financial summary: ").strip()
                goalOrNot = input("Do you have a financial goal that you would like to be analysed in the summary (Y/n)? ").lower()
                try:
                    userDays = int(userDays)
                    if goalOrNot == "y":
                        summary(userDays, True) #include goal in summary
                    else:
                        summary(userDays, False)
                except:
                    print("Invalid input for days. Please enter a number")

            elif userOption == 5:
                print("Exiting program. Hopefully see you soon!")
                main = False

            else:
                print("Invalid option. Please enter a number between 1 and 5")

        except:
            print("Invalid input. Please enter a number between 1 and 5")

mainMenu()