import rules
import globals
import random
import string
# note: cannot import points in here, so some points management happening here

# Note: marble name fields may get out of sync here due to swapping, did not synchronize it,
# likely unnecessary since it doesn't ever get printed

# Note: TODO we do need to maintain marble placements

lastSpinner = ""

def adamSuppBard():
    prevSupp = rules.getRole("support")
    print("Swapping Adam to support bard, swapping "+prevSupp+" to Adam's old assignment")
    globals.summoners[prevSupp].curMarble = globals.summoners["Adam"].curMarble
    globals.summoners["Adam"].curMarble = rules.addSuppBard("Adam")

def kayTop():
    print(rules.RED_TXT_START+"NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print("sad ;;"+rules.DEF_TXT_END)
    prevTop = rules.getRole("top")
    print("Swapping Kay to top, swapping "+prevTop+" to Kay's old assignment")
    temp = globals.summoners[prevTop].curMarble
    globals.summoners[prevTop].curMarble = globals.summoners["Kaylia"].curMarble
    globals.summoners["Kaylia"].curMarble = temp

def rageBot():
    prevBot = rules.getRole("bot")
    print("Swapping Rage to ADC bot, swapping "+prevBot+" to Rage's old assignment")
    globals.summoners[prevBot].curMarble = globals.summoners["Rage"].curMarble
    globals.summoners["Rage"].curMarble = rules.addADCBot("Rage")

def bankruptPerson():
    name = globals.inputSummoner()
    globals.summoners[name].money = 0

def swapMoney():
    name1 = globals.inputSummoner()
    name2 = globals.inputSummoner()
    temp = globals.summoners[name1].money
    globals.summoners[name1].money = globals.summoners[name2].money
    globals.summoners[name2].money = temp

def take50Dollars():
    name = globals.inputSummoner()
    globals.summoners[name].money -= 50
    globals.summoners[lastSpinner].money += 50

def printChoosable(victims):
    print()
    print("Choosable people: ")
    print(victims)
    
    for victim in victims:
        rules.printMarbles([globals.summoners[victim].curMarble])

def changeLvl1Letter():
    victims = rules.getLvl1s()
    changeLetter(victims)

def changeLetter(victims, isRandom=False):
    victim = ""
    if(len(victims) == 0):
        print("No one has a lvl 1 marble")
        return
    elif(len(victims) == 1):
        victim = victims[0]
    else:
        printChoosable(victims)
        victim = globals.inputSummoner(victims)
    
    letter = ""
    if(isRandom):
        letter = random.choice(string.ascii_uppercase)
    else:
        while True:
            letter = input("Pick a letter: ").strip()
            if not (len(letter) == 1 and letter.isalpha()):
                print("Dumbass. Enter a letter.")
                continue
            break
    rules.changeLetter(globals.summoners[victim].curMarble, letter)

# Note: if you change letter to "" then it gives them freedom
def changeLetters():
    victims = rules.getHasLetters()
    if(len(victims)<2):
        print("Not enough people with letters.")
        return
    
    # todo add prints
    name1 = globals.inputSummoner(victims)
    name2 = globals.inputSummoner(victims)
    letter1 = rules.marbles[globals.summoners[name1].curMarble].letter
    letter2 = rules.marbles[globals.summoners[name2].curMarble].letter
    rules.changeLetter(globals.summoners[name2].curMarble, letter1)
    rules.changeLetter(globals.summoners[name1].curMarble, letter2)

def changeRoles():
    name1 = globals.inputSummoner()
    name2 = globals.inputSummoner()
    role1 = rules.marbles[globals.summoners[name1].curMarble].position
    role2 = rules.marbles[globals.summoners[name2].curMarble].position
    rules.changeRole(globals.summoners[name2].curMarble, role1)
    rules.changeRole(globals.summoners[name1].curMarble, role2)

def freedomRoleSteal():
    role = ""
    while True:
        role = input("Role to steal?").lower()
        if not role in globals.ROLES:
            print("That's not a valid role, try again")
            continue
        break
    # take role
    if(role != rules.marbles[globals.summoners[lastSpinner].curMarble].position):
        rules.forceTakeRole(lastSpinner, role)
    
    # lose letter restriction
    rules.changeLetter(globals.summoners[lastSpinner].curMarble, "")

def marbleDec():
    victims = rules.getNoLetters()
    changeLetter(victims, True)

def marbleLargeDec():
    name = globals.inputSummoner()
    rules.forceNextLvl1(name)

def marbleInc():
    oldLvl = rules.marbles[globals.summoners[lastSpinner].curMarble].level
    print("Previous marble level: "+oldLvl)
    if(oldLvl == "1"):
        freedomRoleSteal()
    elif(oldLvl == "2"):
        marbleLargeInc()
    elif(oldLvl == "3" or oldLvl == "4"):
        message = lastSpinner+" has become MARBLE GOD!"
        print(rules.GREEN_TXT_START+message+rules.DEF_TXT_END) # TODO might cause issues with further wheel spins?
        rules.assignMarblePlaceholders(message)
        
def marbleLargeInc():
    rules.changeLetter(globals.summoners[lastSpinner].curMarble, "")

def nop():
    pass

wheel_map = {
    "Adam swaps with support and plays bard": adamSuppBard, # ok
    "Bankrupt someone of your choice": bankruptPerson,
    "Change the letter for someone's Lvl1 Marble": changeLvl1Letter, # ok
    "Force two people with letters to trade letters (roles stay the same)": changeLetters, # ok
    "Force two people to trade roles (letters stay the same)": changeRoles,
    "Freedom (can boot someone off role and they take next same lvl marble for available role.)": freedomRoleSteal, # ok
    "JON & ADAM SHOT NOW": nop,
    "MARBLE GOD": nop, # todo role placeholders
    "Marble - add random letter restriction to someone without one": marbleDec,
    "Marble -- force someone onto their next lvl1 marble of current role": marbleLargeDec, # ok
    "Marble + (1->2 can boot people off of role, 2->LETTER FREEDOM, 3 or 4->MARBLE GOD, 0->nothing)": marbleInc, # ok
    "Marble ++ (LETTER FREEDOM, roles don't change)": marbleLargeInc, # ok
    "raguyamotha swaps marbles with bot and has to play an actual ADC": rageBot, # ok
    "SCRAP MARBLES THE HOMIES NEED HELP": nop, # todo role placeholders
    "Swap the money of two people": swapMoney,
    "Take $50 away from someone and keep it (can put them negative)": take50Dollars, # ok
    "Top lane trades marble with Kay": kayTop #ok
}