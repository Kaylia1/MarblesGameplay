import os
import backendTools.globals as globals
import re
import backendTools.parseChampStats as parseChampStats
# import tkChampStats

MARBLES_OUTPUT = "./data/marbles_output.txt"
MARBLES_OPTIONS = "./data/MoneyMarbles.txt"

marbles = []

godScenario = False
marblesExist = False
bestVision = ""

GREEN_TXT_START = "\033[1;32;40m "
DEF_TXT_END = " \033[0m"
RED_TXT_START = "\033[31m"

# =============== custom QOL for this file ===============

def myinput(prompt):
    res = input(prompt)
    # if res == ".": # TODO UI
    #     tkChampStats.update_app(marbleChampStats())
    return res

# =============== marble logic ==========================
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

# Sets the global marbles variable by parsing large text input
# return True if successful or False if unsuccessful
def readMarbles(marblesData):    
    global marblesExist
    print("READING")
    
    lines = marblesData.strip().splitlines()

    # Marbles output is in format marbleTitle | 0 | time, we only care about title
    # Parse the entire marbles output
    global marbles
    marbles = []
    for i, line in enumerate(lines):
        if line.strip() == "": # skip whitespace lines
            print("skipping whitespace line")
            continue
        line = re.split(r"[ \t]+", line.strip())
        if len(line) < 3:
            return False
        line.pop() # remove time data
        line.pop() # remove history placement data
        line = " ".join(line)
        
        splitted = line.split("Lvl")
        if len(splitted) < 2:
            return False
        level = splitted[1]
        values = splitted[0].split(" ")
        if len(values) < 1:
            return False
        name = values[0]
        marbles.append(Marble(name, line, level, i, values))
    marblesExist = True
    return True

def marbleChampStats():
    appData = []
    # For each summoner, get the array of champs for them
    for summonerName in globals.allSummoners:
        letter = marbles[globals.summoners[summonerName].curMarble].letter
        role = marbles[globals.summoners[summonerName].curMarble].position
        appData.append(parseChampStats.getChamps(letter, role))
    return appData

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
    print("Failed to get top marble for "+summonerName+" starting from "+str(startPoint)+" lvl"+level)
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
    
# TODO note this messes up letter, so it can no longer be used as letter
def assignMarblePlaceholders(message):
    global marbles
    global godScenario
    godScenario = True
    for summoner in globals.summoners.values():
        marbles.append(MarbleAssignment(summoner.name, message, letter=message, level="INF"))
        summoner.curMarble = len(marbles)-1

# for paralyzed states
# input startPoint as the i of the current marble to find new marbles after it
def getTopSummonerMarbles(summonerName, startPoint, unpickedRoles, level, numMarbles):
    nextPossibleMarble = startPoint
    possibleMarbles = []
    for i in range(numMarbles):
        nextPossibleMarble = getBestMarble(summonerName, level, nextPossibleMarble+1, unpickedRoles)
        possibleMarbles.append(nextPossibleMarble)
    return possibleMarbles

def setCurMarble(summonerName, marbleNum):
    globals.summoners[summonerName].curMarble = marbleNum

def setRole(marble, newRole):
    global marbles
    marbles[marble].position = newRole

def setLvl(marble, lvl):
    global marbles
    marbles[marble].level = lvl

def printMarbles(marbleList):
    for i in range(len(marbleList)):
        print(str(i)+": "+marbles[marbleList[i]].marbleDesc)

def printTop10Marbles():
    print("Top 10 marbles:")
    for i in range(10):
        print(str(i)+": "+marbles[i].marbleDesc)

def top1Swaper(swapNum):
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

def bestVisionSwaper(marbleNum):
    if bestVision == "":
        print("WARN: No one has best vision")
        return
    # assign person with bestVision to the marble at swapNum
    globals.summoners[bestVision].curMarble = marbleNum
    if marbles[marbleNum].isMarbleGod():
        global godScenario
        godScenario = True
        assignMarblePlaceholders(bestVision + " is the marble god")

def updatePickList(unpickedSummoners, picker, unpickedRoles, pickedRole):
    unpickedSummoners.remove(picker)
    if(pickedRole in unpickedRoles):
        unpickedRoles.remove(pickedRole)
    
# returns True on success or False on failure
def initGetBestMarbles():
    global godScenario
    # initialize god scenario as false at start of selection
    godScenario = False
    for summoner in globals.summoners.values():
        summoner.curMarble = getBestMarble(summoner.name)
        if summoner.curMarble < 0: # Failed to parse for that name
            return False
        if(marbles[summoner.curMarble].isMarbleGod()):
            print(summoner.name + " has won marble god!")
            godScenario = True
            assignMarblePlaceholders(summoner.name + " is the marble god")
            return True
    return True # not marble god, exit normally
    
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
    marbles.append(MarbleAssignment(name=summonerName, marbleDesc="wheel support bard", letter="BARD", position="support", level="INF"))
    return len(marbles) - 1

def addADCBot(summonerName):
    global marbles
    marbles.append(MarbleAssignment(name=summonerName, marbleDesc="wheel adc adc", letter="ADC", position="bot", level="INF"))
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
