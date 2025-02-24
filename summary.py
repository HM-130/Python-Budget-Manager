import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from crud import readFile

def getThresholdDate(days):
    currentDate = datetime.date.today()
    thresholdDate = currentDate - datetime.timedelta(days=days) #the amount of days back the summary is of
    return thresholdDate


#function to turn dates to uk format
def parseDate(date_str):
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()


def longTermIncomesAndExpenses():
    lines = readFile("longTerm.csv")
    incomeSum = 0
    expenseSum = 0
    incomeSources = {}
    expenseSources = {}
    goal = None
    goalFound = False
    for line in lines:
        tupleLine = tuple(line.strip().split(","))
        if tupleLine[1] == "Income":
            incomeSum += float(tupleLine[3])
            if tupleLine[4] in incomeSources:
                incomeSources[tupleLine[4]] += float(tupleLine[3])
            else:
                incomeSources[tupleLine[4]] = float(tupleLine[3])
        elif tupleLine[1] == "Expense":
            expenseSum += float(tupleLine[3])
            if tupleLine[4] in expenseSources:
                expenseSources[tupleLine[4]] += float(tupleLine[3])
            else:
                expenseSources[tupleLine[4]] = float(tupleLine[3])
        else:
            if goalFound:
                print("\nError reading longTerm.csv - only one goal allowed")
            else:
                goal = tupleLine
                goalFound = True

    print("\nLong term stats:")
    print(f"Your total long term income (monthly and yearly) is £{incomeSum}")
    print(f"Your total long term expense (monthly and yearly) is £{expenseSum}")
    return incomeSources, expenseSources, goal #for use in pie chart function and financialGoalStatus function


def getValuesWithinTime(incomeOrExpenses, startDate, endDate):
    dateIndex = 0
    if incomeOrExpenses == "Incomes":
        dateIndex = 1
        lines = readFile("incomes.csv")
    elif incomeOrExpenses == "Expenses":
        dateIndex = 2
        lines = readFile("transactions.csv")
    else:
        print("\nInvalid entry for incomeOrExpenses - getValuesWithinDateRange")
        return None

    valuesWithinRange = []
    for line in lines:
        tupleLine = tuple(line.strip().split(","))  #convert line to tuple for ease of access
        lineDate = parseDate(tupleLine[dateIndex])  #parse string date to datetime object in uk format
        if startDate <= lineDate <= endDate:
            valuesWithinRange.append(tupleLine)
    if len(valuesWithinRange)==0:
        print(f"No values found for {incomeOrExpenses} between {startDate} and {endDate}")
    return valuesWithinRange


def outputValuesAndTotal(incomeOrExpenses, valuesWithinTime, days): 
    if incomeOrExpenses == "Incomes":
        amounts = []
        print(f"\n{len(valuesWithinTime)} individual incomes over the last {days} days")
        print(f"Incomes over the last {days} days:")
        for line in valuesWithinTime:
            print(f"ID: {line[0]}, Date: {line[1]}, Amount Gained: £{line[2]}")
            amounts.append(float(line[2]))
        sumOfIncome = sum(amounts)
        print(f"Total income over the last {days} days: £{sumOfIncome}")
        return sumOfIncome

    elif incomeOrExpenses == "Expenses":
        amounts = []
        print(f"\n{len(valuesWithinTime)} individual transactions over the last {days} days")
        print(f"Transactions over the last {days} days:")
        for line in valuesWithinTime:
            print(f"ID: {line[0]}, Category: {line[1]}, Date: {line[2]}, Location: {line[3]}, Amount Spent: £{line[4]}")
            amounts.append(float(line[4]))
        sumOfExpenses = sum(amounts)
        print(f"Total expense over the last {days} days: £{sumOfExpenses}")
        return sumOfExpenses
    
    else:
        print("Error in incomeOrExpenses - outputValuesAndTotal")


def locationPercentages(transactionsWithinTime, sumOfExpenses):
    percentagesAtLocations = {}
    for line in transactionsWithinTime:
        decimal = float(line[4])/sumOfExpenses
        percentage = decimal * 100
        if line[3] in percentagesAtLocations:
            newPercentage = float(percentagesAtLocations[line[3]]) + percentage
            percentagesAtLocations[line[3]] = round(newPercentage, 1)
        else:
            percentagesAtLocations[line[3]] = round(percentage, 1)

    sortedPercentagesAtLocations = sorted(percentagesAtLocations.items(), key=lambda item: item[1], reverse=True) #sorts dictionary based on value size in descending order

    print("\nHere are the locations you have spent money at and the percentage of your total expenses spent at each one, in descending order:")
    for k, v in sortedPercentagesAtLocations:
        print(f"Location: {k}, Percentage: {v}%")
    return dict(sortedPercentagesAtLocations) #for use in pieChart function


def categoryByAmountOfTransactions(transactionsWithinTime):
    #writes the amount of transactions in each category to a dict
    categorySums = {}
    for line in transactionsWithinTime:
        if line[1] in categorySums:
            categorySums[line[1]] += 1
        else:
            categorySums[line[1]] = 1

    sortedCategorySums = sorted(categorySums.items(), key=lambda item: item[1], reverse=True) #sorts dictionary based on value size in descending order

    print("\nHere are the categories you have spent money in and the percentage of your total transactions in each category, in descending order:")
    for k, v in sortedCategorySums:
        percentage = round(v/len(transactionsWithinTime)*100, 1)
        print(f"Category: {k}, Amount of Transactions: {v}, Percentage of transactions in category: {percentage}%")
    return dict(sortedCategorySums) #for use in pieChart function


def getBalance(sumofIncomes, sumofExpenses):
    balance = sumofIncomes - sumofExpenses
    if balance<0:
        print(f"\nYou are in £{balance} of debt, consider lowering your spending in unnecessary categories")
    else:
        print(f"\nRemaining balance: £{balance}")


def financialGoalStatus(goal):
    print("\nFinancial Goal Analysis:")
    if not goal or len(goal)<5:
        print("No financial goal set.")
        return
    
    currentDate = datetime.date.today()
    startDate = parseDate(goal[4])  #date when goal starts
    timePeriod, targetAmount = goal[2].lower(), float(goal[3])

    #goal duration
    if timePeriod == "monthly":
        endDate = startDate + relativedelta(months=1)
    else:  #assume yearly if not monthly
        endDate = startDate + relativedelta(months=12)

    goalInPlay = True
    if endDate < currentDate: #if the goal range has passed
        print("Your goal end date has passed! Lets see how you did:")
        goalInPlay = False
        incomes = getValuesWithinTime("Incomes", startDate, endDate)
        expenses = getValuesWithinTime("Expenses", startDate, endDate)
    else:
        timeLeft = (endDate-currentDate).days
        print(f"You still have {timeLeft} day(s) left to work towards your goal! Lets see how you're doing:")
        incomes = getValuesWithinTime("Incomes", startDate, currentDate) #if goal is still in play, check savings between current date and starting date
        expenses = getValuesWithinTime("Expenses", startDate, currentDate)

    incomeSum = 0
    for line in incomes:
        incomeSum += float(line[2])
    expenseSum = 0
    for line in expenses:
        expenseSum += float(line[4])
    netSavings = round(incomeSum - expenseSum, 2)

    progress = round((netSavings / targetAmount) * 100, 2)

    print(f"Goal start date: {startDate.strftime('%d/%m/%Y')}, End date: {endDate.strftime('%d/%m/%Y')}")
    print(f"Your {timePeriod} goal: £{targetAmount} saved")
    if netSavings >= targetAmount:
        if goalInPlay:
            print(f"Your net savings from {startDate.strftime('%d/%m/%Y')} to today: £{netSavings}")
            print(f"Look at you! You hit your {timePeriod} goal before the time period was even over!\n")
        else:
            print(f"Your net savings from {startDate.strftime('%d/%m/%Y')} to {endDate.strftime('%d/%m/%Y')}: £{netSavings}")
            print(f"Congratulations! You hit your {timePeriod} goal successfully between {startDate.strftime('%d/%m/%Y')} and {endDate.strftime('%d/%m/%Y')}!")
            print(f"To set a new goal, return to menu and update your existing goal, or delete and add a new one\n")
    else:
        if goalInPlay:
            print(f"Your net savings from {startDate.strftime('%d/%m/%Y')} to today: £{netSavings}")
            remaining = round(targetAmount - netSavings, 2)
            print(f"Keep going! You're at {progress}% of your {timePeriod} goal, you need £{remaining} more to reach it\n")
        else:
            print(f"Your net savings from {startDate.strftime('%d/%m/%Y')} to {endDate.strftime('%d/%m/%Y')}: £{netSavings}")
            remaining = round(targetAmount - netSavings, 2)
            print(f"You failed to complete your {timePeriod} goal between {startDate.strftime('%d/%m/%Y')} and {endDate.strftime('%d/%m/%Y')}, better luck next time!")
            print(f"To set a new goal, return to menu and update your existing goal, or delete and add a new one\n")


def pieChart(ax, dict, title, description): #ax being the location of the pie chart in 2X2 grid
    labels = list(dict.keys())
    sizes = list(dict.values())
    #autopct=format of labels, pctdistance=label distance from chart, colors=plt.cm.Paired.colors uses different colours 
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors, pctdistance=0.85)
    ax.set_title(title)
    #0=x coordinate of each ax, -1.3=y coordinate (- to be below chart), ha/va are horizontal and vertical alignment
    ax.text(0, -1.3, description, ha='center', va='center', fontsize=10) 


def summary(days, goalOrNot):
    print(f"\nFinancial Summary of the last {days} days")
    endDate = datetime.date.today()
    startDate = endDate - datetime.timedelta(days=days)
    incomeAndExpenseSources = longTermIncomesAndExpenses()
    incomeSources, expenseSources, goal = incomeAndExpenseSources
    print(incomeSources)
    print(expenseSources)
    print(goal)

    incomesWithinTime = getValuesWithinTime("Incomes", startDate, endDate)
    sumofIncomes = outputValuesAndTotal("Incomes", incomesWithinTime, days)

    transactionsWithinTime = getValuesWithinTime("Expenses", startDate, endDate)
    sumofExpenses = outputValuesAndTotal("Expenses", transactionsWithinTime, days)

    percentagesAtLocations = locationPercentages(transactionsWithinTime, sumofExpenses)
    categorySums = categoryByAmountOfTransactions(transactionsWithinTime)

    getBalance(sumofIncomes, sumofExpenses)
    if goalOrNot:
        financialGoalStatus(goal)

    #visual representation
    fig, axes = plt.subplots(2, 2, figsize=(8, 6)) #creates figure with 2X2 subplots
    pieChart(axes[0, 0], incomeSources, "Long Term Income Sources", "Percentages of long-term income from each source")
    pieChart(axes[0, 1], expenseSources, "Long Term Expense Sources", "Percentages of long-term expense from each source")
    pieChart(axes[1, 0], percentagesAtLocations, "Transaction Location Distribution", "Percentages of total expense spent at each location")
    pieChart(axes[1, 1], categorySums, "Transaction Category Distribution", "Percentages of all transactions spent in each category")
    fig.suptitle("Visual Financial Summary", fontsize=18, fontweight='bold')
    plt.tight_layout(pad=1.0) #pad is space between plots
    plt.show()