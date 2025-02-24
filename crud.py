import uuid  #for id

def readFile(fileName):
    with open(fileName, "r") as file:
        lines = file.readlines()[1:]  #skip first line with column titles
        nonNullLines = []
        for line in lines:
            if not line.strip():
                continue
            nonNullLines.append(line)
        return nonNullLines


def addToFile(fileName, data):
    with open(fileName, "a") as file:
        file.write(f"\n{data}")


def generateId():
    return str(uuid.uuid4())[:8]


def addTransaction(category, date, location, amount):
    transactionId = generateId()
    addToFile("transactions.csv", f"{transactionId},{category},{date},{location},{amount}")


def addIncome(date, amount):
    incomeId = generateId()
    addToFile("incomes.csv", f"{incomeId},{date},{amount}")


def addLongTerm(incomeOrExpenseOrGoal, timePeriod, amount, source):
    longTermId = generateId()
    addToFile("longTerm.csv", f"{longTermId},{incomeOrExpenseOrGoal},{timePeriod},{amount},{source}")


def viewTransactions():
    lines = readFile("transactions.csv")
    for line in lines:
        transactionId, category, date, location, amount = line.strip().split(",")
        print(f"ID: {transactionId}, Category: {category}, Date: {date}, Location: {location}, Amount Spent: £{amount}")


def viewIncome():
    lines = readFile("incomes.csv")
    for line in lines:
        incomeId, date, amount = line.strip().split(",")
        print(f"ID: {incomeId}, Date: {date}, Income: £{amount}")


def viewLongTerm():
    lines = readFile("longTerm.csv")
    for line in lines:
        longTermId, incomeOrExpense, timePeriod, amount, source = line.strip().split(",")
        print(f"ID: {longTermId}, Type: {incomeOrExpense}, Time Period: {timePeriod}, Amount: £{amount}, Source: {source}")


def updateTransaction(updateId, updateCategory, updateDate, updateLocation, updateAmount):
    updated = False
    lines = readFile("transactions.csv")
    for line in lines:
        transactionId, category, date, location, amount = line.strip().split(",")
        if transactionId == updateId:
            addToFile("transactions.csv", f"{updateId},{updateCategory},{updateDate},{updateLocation},{updateAmount}")
            updated = True
        else:
            addToFile("transactions.csv", f"{transactionId},{category},{date},{location},{amount}")
    return updated


def updateIncome(updateId, updateDate, updateAmount):
    updated = False
    lines = readFile("incomes.csv")
    for line in lines:
        incomeId, date, amount = line.strip().split(",")
        if incomeId == updateId:
            addToFile("incomes.csv", f"{updateId},{updateDate},{updateAmount}")
            updated = True
        else:
            addToFile("incomes.csv", f"{incomeId},{date},{amount}")
    return updated 


def updateLongTerm(updateId, updateIncomeOrExpense, updateTimePeriod, updateAmount, updateSource):
    updated = False
    lines = readFile("longTerm.csv")
    for line in lines:
        longTermId, incomeOrExpense, timePeriod, amount, source = line.strip().split(",")
        if longTermId == updateId:
            addToFile("longTerm.csv", f"{updateId},{updateIncomeOrExpense},{updateTimePeriod},{updateAmount},{updateSource}")
            updated = True
        else:
            addToFile("longTerm.csv", f"{longTermId},{incomeOrExpense},{timePeriod},{amount},{source}")
    return updated


def deleteTransaction(deleteId):
    deleted = False
    lines = readFile("transactions.csv")
    existingIds = []
    for line in lines:
        transactionId, category, date, location, amount = line.strip().split(",")
        existingIds.append(transactionId)
    if deleteId not in existingIds:
        return False 
    for line in lines:
        transactionId, category, date, location, amount = line.strip().split(",")
        if transactionId == deleteId:
            deleted = True
            continue
        else:
            addToFile("transactions.csv", f"{transactionId},{category},{date},{location},{amount}")
    return deleted


def deleteIncome(deleteId):
    deleted = False
    lines = readFile("incomes.csv")
    existingIds = []
    for line in lines:
        incomeId, date, amount = line.strip().split(",")
        existingIds.append(incomeId)
    if deleteId not in existingIds:
        return False  
    for line in lines:
        incomeId, date, amount = line.strip().split(",")
        if incomeId == deleteId:
            deleted = True
            continue
        else:
            addToFile("incomes.csv", f"{incomeId},{date},{amount}")
    return deleted


def deleteLongTerm(deleteId):
    deleted = False
    lines = readFile("longTerm.csv")
    existingIds = []
    for line in lines:
        longTermId, incomeOrExpense, timePeriod, amount, source = line.strip().split(",")
        existingIds.append(longTermId)
    if deleteId not in existingIds:
        return False  
    for line in lines:
        longTermId, incomeOrExpense, timePeriod, amount, source = line.strip().split(",")
        if longTermId == deleteId:
            deleted = True
            continue
        else:
            addToFile("longTerm.csv", f"{longTermId},{incomeOrExpense},{timePeriod},{amount},{source}")
    return deleted