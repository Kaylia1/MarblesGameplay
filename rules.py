import os
import globals
import re

MARBLES_OUTPUT = "./data/marbles_output.txt"
MARBLES_OPTIONS = "./data/MoneyMarbles.txt"

marbles = []

GREEN_TXT_START = "\033[1;32;40m "
DEF_TXT_END = " \033[0m"
RED_TXT_START = "\033[31m"

class MarbleAssignment:
    def __init__(self, name, marbleDesc, level="", placement=-1, letter="", position=""):
        self.name = name
        self.level = level
        self.letter = letter
        self.position = position
        self.marbleDesc = marbleDesc
        self.placement = placement
        # freedom is Lvl4, god is LvlMARBLE GOD, paralyzed is Lvl0
    
    def isMarbleGod(self):
        return self.level == "MARBLE GOD"

class Marble(MarbleAssignment):
    def __init__(self, name, marbleDesc, level, placement, values):
        super().__init__(name, marbleDesc, level, placement, "", "",)
        self.values = values
        self.parseMarble()

    # TODO error checking, return success or failure
    # populate MarbleAssignment
    def parseMarble(self):
        # newMarble = Marble(self.name, "", "", level)
        if(self.level == "1"):
            self.letter = self.values[1]
            self.position = self.values[2].lower()
        elif(self.level == "2"):
            self.letter = self.values[1]
        elif(self.level == "3"):
            self.position = self.values[1].lower()
        return True

# TODO should prob be static
def isLevelAssignedPosition(level):
    return level == "1" or level == "3"

def readMarbles():    
    lines = []
    with open(MARBLES_OUTPUT, 'r') as file:
        lines = file.readlines()

    # Marbles output is in format marbleTitle | 0 | time, we only care about title
    # Parse the entire marbles output
    global marbles
    marbles = []
    for i, line in enumerate(lines):
        line = re.split(r"[ \t]+", line.strip())
        line.pop() # remove time data
        line.pop() # remove history placement data
        line = " ".join(line)
        
        splitted = line.split("Lvl")
        level = splitted[1]
        values = splitted[0].split(" ")
        name = values[0]
        marbles.append(Marble(name, line, level, i, values))

def currentMarbleAssignments(unpickedSummoners=list(globals.summoners.keys())):
    print("======")
    for summoner in globals.summoners.values():
        message = summoner.name + ": position: "+marbles[summoner.curMarble].position+" letter: "+marbles[summoner.curMarble].letter+" level: "+marbles[summoner.curMarble].level
        if(not summoner.name in unpickedSummoners):
            message = GREEN_TXT_START+message+DEF_TXT_END
        print(message)
    print("======")

def debugCurrentMarbleAssignments(unpickedSummoners=list(globals.summoners.keys())):
    print("======")
    for summoner in globals.summoners.values():
        message = summoner.name + ": position: "+marbles[summoner.curMarble].position+" letter: "+marbles[summoner.curMarble].letter+" level: "+marbles[summoner.curMarble].level+" original_descriptor: "+marbles[summoner.curMarble].marbleDesc+" original_placement: "+str(marbles[summoner.curMarble].placement)
        if(not summoner.name in unpickedSummoners):
            message = GREEN_TXT_START+message+DEF_TXT_END
        print(message)
    print("======")

def getBestMarble(summonerName, level="-1", startPoint=0, unpickedRoles=globals.ROLES):
    for i in range(startPoint, len(marbles)):
        if(marbles[i].name == summonerName and (level=="-1" or level==marbles[i].level) and (marbles[i].position in unpickedRoles or marbles[i].position == "")):
            # assign this marble to this person
            return i
    print("Failed to get top marble for "+summonerName+" starting from "+startPoint+" lvl"+level)
    return -1

def updateBestMarble(unpickedSummoners, unpickedRoles):
    # if unpicked summoner is currently assigned a taken role, get them a new marble of same level until they get a valid marble
    for summonerName in unpickedSummoners:
        if(not marbles[globals.summoners[summonerName].curMarble].position in unpickedRoles and not marbles[globals.summoners[summonerName].curMarble].position == ""):
            # taken role
            newMarble = getBestMarble(summonerName, marbles[globals.summoners[summonerName].curMarble].level, marbles[globals.summoners[summonerName].curMarble].placement+1, unpickedRoles)
            globals.summoners[summonerName].curMarble = newMarble

def sortByPlacement(item):
    return marbles[globals.summoners[item].curMarble].placement

# note: this naturally makes paralyzed players pick last
def getNextPicker(validSummoners):
    # based on highest marble level that isn't god marble, tiebreak with marble ranking
    highestLevel = 0
    for summonerName in validSummoners:
        level = marbles[globals.summoners[summonerName].curMarble].level
        if(level.isdigit() and int(level) > highestLevel):
            highestLevel = int(level)
    
    # look for summoners with that level
    highLvlSummoners = []
    for summonerName in validSummoners:
        if(marbles[globals.summoners[summonerName].curMarble].level == str(highestLevel)):
            highLvlSummoners.append(summonerName)
    highLvlSummoners = sorted(highLvlSummoners, key=sortByPlacement)
    
    isParalyzed = highestLevel == 0
    if(not isLevelAssignedPosition(str(highestLevel))):
        return highLvlSummoners, isParalyzed
    else:
        return [highLvlSummoners[0]], isParalyzed
    
def assignMarblePlaceholders(message):
    global marbles
    for summoner in globals.summoners.values():
        marbles.append(MarbleAssignment(summoner.name, message))
        summoner.curMarble = len(marbles)-1

# for paralyzed states
# input startPoint as the i of the current marble to find new marbles after it
def getTop5Marbles(summonerName, startPoint, unpickedRoles):
    nextPossibleMarble = startPoint
    possibleMarbles = []
    for i in range(5):
        nextPossibleMarble = getBestMarble(summonerName, "1", nextPossibleMarble+1, unpickedRoles)
        possibleMarbles.append(nextPossibleMarble)
    return possibleMarbles

def pickFromTop5Marbles(summonerName, top5marbles):
    while True:
        marbleNum = input("Choose a marble 0-4 from the list")
        if(not marbleNum.isdigit() or int(marbleNum) < 0 or int(marbleNum) > 4):
            print("Invalid input, needs to be numeric value 0-4")
            continue
        globals.summoners[summonerName].curMarble = top5marbles[int(marbleNum)]
        break

def printMarbles(marbleList):
    for i in range(len(marbleList)):
        print(str(i)+": "+marbles[marbleList[i]].marbleDesc)

def printTop10Marbles():
    print("Top 10 marbles:")
    for i in range(10):
        print(str(i)+": "+marbles[i].marbleDesc)

def top1Swap():
    global marbles
    # Top 1 can choose to swap marbles with any of the top 10 marbles
    printTop10Marbles()
    swapNum = 0
    while True:
        swapNum = input(marbles[0].name + " is top 1, enter the number 0-9 of the marble to swap with.")
        try:
            swapNum = int(swapNum)
            if(swapNum > 9 or swapNum < 0):
                print("That's not in the top 10, try again")
                continue
            elif(marbles[swapNum].level == "MARBLE GOD"):
                print("Can't swap with God, try again")
                continue
            break
        except ValueError:
            print("That's not a valid integer, try again")
    
    # swap marble positions in ranking
    temp = marbles[swapNum]
    marbles[swapNum] = marbles[0]
    marbles[0] = temp
    
    tempName = marbles[swapNum].name
    marbles[swapNum].name = marbles[0].name
    marbles[0].name = tempName
    
    tempPlacement = marbles[swapNum].placement
    marbles[swapNum].placement = marbles[0].placement
    marbles[0].placement = tempPlacement

# if no role assigned, user picks a role
def pickRole(summonerName, unpickedRoles):
    global marbles
    
    # force assign this role
    if(len(unpickedRoles)==1):
        print("One role remaining. Forcibly assigning "+summonerName+" to "+unpickedRoles[0])
        marbles[globals.summoners[summonerName].curMarble].position = unpickedRoles[0]
        return unpickedRoles[0]
    
    # if(not marbles[globals.summoners[summonerName].curMarble].position in unpickedRoles):
    if(marbles[globals.summoners[summonerName].curMarble].position==""):
        # no role assigned yet, can pick own role, input role
        while True:
            print("Remaining roles:")
            print(unpickedRoles) # TODO make this print nicer
            role = input("Role for "+summonerName+"?").lower()
            if not role in unpickedRoles:
                print("That's not a valid role, try again")
            else:
                marbles[globals.summoners[summonerName].curMarble].position = role
                return role
    # elif(not marbles[globals.summoners[summonerName].curMarble].position in unpickedRoles):
    #     # role assigned but taken, fetch next marble
    return marbles[globals.summoners[summonerName].curMarble].position

def updatePickList(unpickedSummoners, picker, unpickedRoles, pickedRole):
    unpickedSummoners.remove(picker)
    if(pickedRole in unpickedRoles):
        unpickedRoles.remove(pickedRole)

def pick(picker, isParalyzed, unpickedSummoners, unpickedRoles):
    # print current state
    currentMarbleAssignments(unpickedSummoners)
    
    # check if current role assignment is ok, else get new marble
    updateBestMarble(unpickedSummoners, unpickedRoles)
    
    print("picker:"+picker)
    # if paralyzed, print next 5 lvl1 marbles of that person with avail roles
    top5 = []
    if isParalyzed:
        top5 = getTop5Marbles(picker, globals.summoners[picker].curMarble, unpickedRoles)
        printMarbles(top5)
        pickFromTop5Marbles(picker, top5)
    pickedRole = pickRole(picker, unpickedRoles)
    
    updatePickList(unpickedSummoners, picker, unpickedRoles, pickedRole)
    

def assignMarbles():
    # Get the top marble for ea of 5 ppl.
    # Check if any person's top 1 is marble god
    readMarbles()
    
    # clear old assignments and get toppmost marble
    for summoner in globals.summoners.values():
        summoner.curMarble = getBestMarble(summoner.name)
        if(marbles[summoner.curMarble].isMarbleGod()):
            print(summoner.name + " has won marble god!")
            assignMarblePlaceholders(summoner.name + " is the marble god")
            return
    
    unpickedSummoners = list(globals.summoners.keys())
    unpickedRoles = list(globals.ROLES)
    currentMarbleAssignments(unpickedSummoners)
    
    top1Swap()
    
    # assign marbles via marble level and picking
    # note: top 1 doesn't pick first ONLY if paralyzed
    if(not marbles[0].level == "0"):
        pick(marbles[0].name, False, unpickedSummoners, unpickedRoles)
    while(len(unpickedSummoners)>0):
        nextPickers, isParalyzed = getNextPicker(unpickedSummoners)
        for picker in nextPickers:
            print(unpickedRoles)
            pick(picker, isParalyzed, unpickedSummoners, unpickedRoles)
            
    print("All positions are assigned:")
    currentMarbleAssignments(unpickedSummoners)
    
    
# ====== wheel helper functions ======
def getRole(role): # return summonerName
    for summoner in globals.summoners.values():
        if marbles[summoner.curMarble].position == role:
            return summoner.name
    return ""

def getNoLetters():
    noletters = []
    for summoner in globals.summoners.values():
        if marbles[summoner.curMarble].letter == "":
            noletters.append(summoner.name)
    return noletters

def getHasLetters():
    noLetters = getNoLetters()
    return list(set(globals.allSummoners) - set(noLetters))

def addSuppBard(summonerName):
    global marbles
    marbles.append(MarbleAssignment(name=summonerName, marbleDesc="wheel support bard", letter="BARD", position="support"))
    return len(marbles) - 1

def addADCBot(summonerName):
    global marbles
    marbles.append(MarbleAssignment(name=summonerName, marbleDesc="wheel adc adc", letter="ADC", position="bot"))
    return len(marbles) - 1

def getLvl1s(): # return array of names
    lvl1s = []
    for summoner in globals.summoners.values():
        if marbles[summoner.curMarble].level == "1":
            lvl1s.append(summoner.name)
    return lvl1s

def changeLetter(i, letter):
    marbles[i].letter = letter 

def changeRole(i, role):
    marbles[i].position = role

def forceTakeRole(summonerName, role):
    # boot someone off of role to next marble of same marble lvl
    # if person is already in role, do nothing
    oldRole = marbles[globals.summoners[summonerName].curMarble].position
    victim = getRole(role)
    
    nextMarble = getBestMarble(victim, marbles[globals.summoners[victim].curMarble].level, globals.summoners[victim].curMarble + 1, [oldRole])
    changeRole(nextMarble, oldRole)
    globals.summoners[victim].curMarble = nextMarble
    
    changeRole(globals.summoners[summonerName].curMarble, role)

def forceNextLvl1(summonerName):
    role = marbles[globals.summoners[summonerName].curMarble].position
    nextMarble = getBestMarble(summonerName, "1", globals.summoners[summonerName].curMarble + 1, [role])
    globals.summoners[summonerName].curMarble = nextMarble