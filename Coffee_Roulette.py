import csv
from collections import OrderedDict

# List of people's names - 1 column - 1 name per line - names start on 2nd row
namesListFileName = "NamesList.csv"

#  List of historical matches - 2 columns - 1 name per column - 
#  comma seperated - names start on 2nd row
coffeeRoueletteOldList = "CR_Old_Pairs.csv"


def setupNamesWithPotentialMatches():
    namesList = []
    namesToMatches = OrderedDict()
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
    return namesToMatches

def removeExistingMatches(namesToMatches):
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
    return namesToMatches

def createWeeklyPairings(namesToMatches):
    # Creating a list of matches for specified number of weeks (i)
    weeklyPairings = []
    weeks = 22
    while weeks > 0:
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
        weeklyPairings.append(week)
        weeks -= 1
    return weeklyPairings

def writeWeeklyPairingsToFile(weeklyPairings):
    # open the file in the write mode - list printed as 2 columns
    with open('Coffee_Roulette_Pairings.csv', 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)

        i = 0
        for week in weeklyPairings:
            i += 1
            writer.writerow(['Week'+str(i)])
            weekSorted = []
            for pairing in week:
                line = pairing[0] + '@' + pairing[1]
                weekSorted.append(line)
            weekSorted.sort()
            for pairing in weekSorted:
                writer.writerow(pairing.split('@'))


namesToMatches = setupNamesWithPotentialMatches()
namesToMatches = removeExistingMatches(namesToMatches)
weeklyPairings = createWeeklyPairings(namesToMatches)
writeWeeklyPairingsToFile(weeklyPairings)
