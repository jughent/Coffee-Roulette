import csv
from collections import OrderedDict
import random
import sys

# List of people's names - 1 column - 1 name per line - names start on 2nd row
namesListFileName = sys.argv[1]

#  List of historical matches - 2 columns - 1 name per column - 
#  comma seperated - names start on 2nd row
coffeeRoueletteOldList = sys.argv[2]

numberOfWeeksToGenerate = 22


def setupNamesWithPotentialMatches():
    namesList = []
    namesToMatches = OrderedDict()
    # Creating dictionaries with Names as key and empty array as value
    with open(namesListFileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0: # skip header row
                name = row[0] # accessing the first column in row
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
            if line_count != 0: # skip header row
                name1 = row[0] #abi
                name2 = row[1] #jes
                if name1 in namesToMatches and name2 in namesToMatches:
                    namesToMatches[name1].discard(name2)
            line_count += 1
    return namesToMatches

def createAllPairings(namesToMatches):
    # Creating a list of matches for specified number of weeks
    weeklyPairings = []
    weekNumber = 1
    while weekNumber <= numberOfWeeksToGenerate:
        print(f'{(weekNumber/numberOfWeeksToGenerate)*100}%')
        weeklyPairings.append(createWeekPairings(namesToMatches))
        weekNumber += 1
    return weeklyPairings

def createWeekPairings(namesToMatches):
    while True:
        pairingsForWeek = generateRandomPairingsList(namesToMatches)
        # only stop this loop when everyone has a match.
        # If someone doesn't have a match, `pairingsForWeek` will be false
        if pairingsForWeek:
            break
    # once we find a set of pairings where everyone has a match
    for pairing in pairingsForWeek:
        namesToMatches[pairing[0]].discard(pairing[1])
        namesToMatches[pairing[1]].discard(pairing[0])
    return pairingsForWeek

# generate a list of pairings for a week. Return false if not found
def generateRandomPairingsList(namesToMatches):
    # names of people who have already been matched this week
    alreadyMatchedForThatWeek = set()

    # list of tuples of matches for the week
    pairingsForWeek = []

    # create randomised list of dictionary keys (randomised list of names)
    randomisedNamesToMatches = list(namesToMatches.keys())
    random.shuffle(randomisedNamesToMatches)

    # for each person's name
    for name in randomisedNamesToMatches:
        # get that persons potential matches (access the value at that `name`'s key in `namesToMatches`)
        potentialMatches = namesToMatches[name]

        # if this person has previously been matched with someone this week (ie a match has already selected them)
        # or there are no possible people for them to match with (ie theyve had coffee with everyone already)
        if name in alreadyMatchedForThatWeek or len(potentialMatches) == 0:
            continue

        # assume the person hasn't found a match yet
        hasFoundMatch = False

        # a list of all matches this person hasn't yet had
        # converting potentialMatches from a set to a list so we can sort (cannot order a set)
        potentialMatchesAsList = list(potentialMatches)
        potentialMatchesAsList.sort()

        # potentialMatch is name in the sorted list
        for potentialMatch in potentialMatchesAsList:
            # if the potential match doesn't already have a coffee date this week, this person is the one
            if potentialMatch not in alreadyMatchedForThatWeek:
                # add both pairs of matches to the list
                pairingsForWeek.append((name, potentialMatch))
                pairingsForWeek.append((potentialMatch, name))

                # mark both people as taken for this particular week
                alreadyMatchedForThatWeek.add(name)
                alreadyMatchedForThatWeek.add(potentialMatch)

                #mark `hasFoundMatch` as true
                hasFoundMatch = True
                break
        
        # if we're unable to find a match for this person, return false
        if not hasFoundMatch:
            return False

    # if we were able to find a match for everyone, return the matches
    return pairingsForWeek

def writeWeeklyPairingsToFile(weeklyPairings):
    # open the file in the write mode - list printed as 2 columns
    with open('Coffee_Roulette_Pairings.csv', 'w',  newline='', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)

        i = 0
        for week in weeklyPairings:
            i += 1
            writer.writerow([])
            writer.writerow([f'Week {i}, Total matches: {len(week)}'])
            weekSorted = []
            for pairing in week:
                line = pairing[0] + '@' + pairing[1]
                weekSorted.append(line)
            weekSorted.sort()
            for pairing in weekSorted:
                writer.writerow(pairing.split('@'))


namesToMatches = setupNamesWithPotentialMatches()
namesToMatches = removeExistingMatches(namesToMatches)
weeklyPairings = createAllPairings(namesToMatches)
writeWeeklyPairingsToFile(weeklyPairings)
print('all done yeah boy')