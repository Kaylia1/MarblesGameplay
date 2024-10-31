import os
import globals
import re

MARBLES_OUTPUT = "./data/marbles_output.txt"
MARBLES_OPTIONS = "./data/MoneyMarbles.txt"

marbles = []
ROLES = ["jungle", "support", "top", "mid", "bot"]

GREEN_TXT_START = "\033[1;32;40m "
GREEN_TXT_END = " \033[0m"

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

# Don't need to read every marble, optimize by only reading assignments
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
            message = GREEN_TXT_START+message+GREEN_TXT_END
        print(message)
    print("======")

def debugCurrentMarbleAssignments(unpickedSummoners=list(globals.summoners.keys())):
    print("======")
    for summoner in globals.summoners.values():
        message = summoner.name + ": position: "+marbles[summoner.curMarble].position+" letter: "+marbles[summoner.curMarble].letter+" level: "+marbles[summoner.curMarble].level+" original_descriptor: "+marbles[summoner.curMarble].marbleDesc+" original_placement: "+str(marbles[summoner.curMarble].placement)
        if(not summoner.name in unpickedSummoners):
            message = GREEN_TXT_START+message+GREEN_TXT_END
        print(message)
    print("======")

def getBestMarble(summonerName, level="-1", startPoint=0):
    for i in range(startPoint, len(marbles)):
        if(marbles[i].name == summonerName and (level=="-1" or level==marbles[i].level)):
            # assign this marble to this person
            return i
    print("Failed to get top marble for "+summonerName+" starting from "+startPoint+" lvl"+level)
    return -1

def updateBestMarble(unpickedSummoners, unpickedRoles):
    # if unpicked summoner is currently assigned a taken role, get them a new marble of same level until they get a valid marble
    for summonerName in unpickedSummoners:
        if(not marbles[globals.summoners[summonerName].curMarble].position in unpickedRoles and not marbles[globals.summoners[summonerName].curMarble].position == ""):
            # taken role
            newMarble = getBestMarble(summonerName, marbles[globals.summoners[summonerName].curMarble].level, marbles[globals.summoners[summonerName].curMarble].placement+1)
            globals.summoners[summonerName].curMarble = newMarble

def sortByPlacement(item):
    return marbles[globals.summoners[item].curMarble].placement

# TODO can add optimizations here of finding pick order all at once and only needing to reorganize if a role is taken (lvl1 or lvl3)
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
    
    if(not isLevelAssignedPosition(str(highestLevel))):
        return highLvlSummoners
    else:
        return [highLvlSummoners[0]] # can only assign one role
    
def assignMarblePlaceholders(message):
    global marbles
    for summoner in globals.summoners.values():
        marbles.append(MarbleAssignment(summoner.name, message))
        summoner.curMarble = len(marbles)-1

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
    unpickedRoles = list(ROLES)
    currentMarbleAssignments(unpickedSummoners)
    
    top1Swap()
    
    # assign marbles via marble level and picking
    pickedRole = pickRole(marbles[0].name, unpickedRoles)
    updatePickList(unpickedSummoners, marbles[0].name, unpickedRoles, pickedRole)
    updateBestMarble(unpickedSummoners, unpickedRoles)
    while(len(unpickedSummoners)>0):
        nextPickers = getNextPicker(unpickedSummoners)
        for picker in nextPickers:
            # print current state
            currentMarbleAssignments(unpickedSummoners)
            
            print("picker:"+picker)
            # if role is not assigned, choose a role
            pickedRole = pickRole(picker, unpickedRoles)
            updatePickList(unpickedSummoners, picker, unpickedRoles, pickedRole)
            updateBestMarble(unpickedSummoners, unpickedRoles)
            
    print("All positions are assigned:")
    currentMarbleAssignments(unpickedSummoners)
    
    
        
    
    
    

    