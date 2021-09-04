import csv
from collections import OrderedDict

namesListFileName = "NamesList.csv"
coffeeRoueletteOldList = "CR_Old_Pairs.csv"

namesToMatches = OrderedDict()
namesList = []

# Creating dictionaries with Names as key and empty array as value
with open(namesListFileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Header Row")
        else:
            name = row[0]
            namesList.append(name)
        line_count += 1
    for name in namesList:
        namesToMatches[name] = set(namesList)
        namesToMatches[name].remove(name)
        


with open(coffeeRoueletteOldList) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Header Row")
        else:
            name1 = row[0] #abi
            name2 = row[1] #jes
            if name1 in namesToMatches and name2 in namesToMatches:
                namesToMatches[name1].discard(name2)
        line_count += 1
# print(namesToMatches)

# weeks = [[(Julia, Josh), (John, Will)], [(Julia, Will), (Josh, John)]]
weeks = []

i = 22
while i > 0:
    week = []
    taken = set()
    for name, potentialMatches in namesToMatches.items():
        if name in taken or len(potentialMatches) == 0:
            continue
        hasFoundMatch = False
        potentialMatchesAsList = list(potentialMatches)
        potentialMatchesAsList.sort()
        for potentialMatch in potentialMatchesAsList:
            if potentialMatch not in taken:
                matchName = potentialMatch
                potentialMatches.remove(potentialMatch)
                hasFoundMatch = True
                break
        if hasFoundMatch:
            namesToMatches[matchName].discard(name)
            week.append((name,matchName))
            week.append((matchName, name))
            taken.add(name)
            taken.add(matchName)
    weeks.append(week)
    i -= 1

# open the file in the write mode
with open('Coffee_Roulette_Pairings.csv', 'w', encoding='UTF8') as f:
    # create the csv writer
    writer = csv.writer(f)

    i = 0
    for week in weeks:
        i += 1
        writer.writerow(['Week'+str(i)])
        weekSorted = []
        for pairing in week:
            line = pairing[0] + '@' + pairing[1]
            weekSorted.append(line)
        weekSorted.sort()
        for pairing in weekSorted:
            writer.writerow(pairing.split('@'))
