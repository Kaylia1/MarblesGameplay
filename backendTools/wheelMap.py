import backendTools.rules as rules
import backendTools.globals as globals
import random
import string
# note: cannot import points in here, so some points management happening here

# Note: marble name fields may get out of sync here due to swapping, did not synchronize it,
# likely unnecessary since it doesn't ever get printed

# Note: TODO we do need to maintain marble placements

lastSpinner = ""

# ========================== TAKES 2 INPUTS ===========================================
def adamSuppBard(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    b = args[1] if len(args) > 1 else None
    
    prevSupp = rules.getRole("support")
    print("Swapping Adam to support bard, swapping " + prevSupp + " to Adam's old assignment")
    globals.summoners[prevSupp].curMarble = globals.summoners["Adam"].curMarble
    globals.summoners["Adam"].curMarble = rules.addSuppBard("Adam")

def kayTop(args):
    if rules.godScenario:
        return
    print(rules.RED_TXT_START + "NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print("sad ;;" + rules.DEF_TXT_END)
    prevTop = rules.getRole("top")
    print("Swapping Kay to top, swapping " + prevTop + " to Kay's old assignment")
    temp = globals.summoners[prevTop].curMarble
    globals.summoners[prevTop].curMarble = globals.summoners["Kaylia"].curMarble
    globals.summoners["Kaylia"].curMarble = temp

def rageBot(args):
    if rules.godScenario:
        return
    prevBot = rules.getRole("bot")
    print("Swapping Rage to ADC bot, swapping " + prevBot + " to Rage's old assignment")
    globals.summoners[prevBot].curMarble = globals.summoners["Rage"].curMarble
    globals.summoners["Rage"].curMarble = rules.addADCBot("Rage")

def bankruptPerson(args):
    a = args[0] if len(args) > 0 else None
    a = a[0].upper() + a[1:].lower()
    globals.summoners[a].money = 0

def swapMoney(args):
    a = args[0] if len(args) > 0 else None
    b = args[1] if len(args) > 1 else None
    a = a[0].upper() + a[1:].lower()
    b = b[0].upper() + b[1:].lower()
    temp = globals.summoners[a].money
    globals.summoners[a].money = globals.summoners[b].money
    globals.summoners[b].money = temp

def take50Dollars(args):
    a = args[0] if len(args) > 0 else None
    a = a[0].upper() + a[1:].lower()
    globals.summoners[a].money -= 50
    globals.summoners[lastSpinner].money += 50

def changeLvl1Letter(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    b = args[1] if len(args) > 1 else None
    victims = rules.getLvl1s()
    changeLetter(victims, a, b)

def changeLetter(victims, a=None, b=None, isRandom=False):
    if rules.godScenario:
        return
    victim = ""
    if len(victims) == 0:
        print("No one has a lvl 1 marble")
        return
    elif len(victims) == 1:
        victim = victims[0]
    else:
        # printChoosable(victims)
        victim = a[0].upper() + a[1:].lower()
    
    letter = random.choice(string.ascii_uppercase) if isRandom else b.upper()
    rules.changeLetter(globals.summoners[victim].curMarble, letter)

def changeLetters(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    b = args[1] if len(args) > 1 else None
    a = a[0].upper() + a[1:].lower()
    b = b[0].upper() + b[1:].lower()
    victims = rules.getHasLetters()
    if len(victims) < 2:
        print("Not enough people with letters.")
        return

    letter1 = rules.marbles[globals.summoners[a].curMarble].letter
    letter2 = rules.marbles[globals.summoners[b].curMarble].letter
    rules.changeLetter(globals.summoners[b].curMarble, letter1)
    rules.changeLetter(globals.summoners[a].curMarble, letter2)
    
    # if unknown level ie "" for freedom or "INF" for special cases, swap level too
    if len(letter1) != 1 or len(letter2) != 1:
        temp = rules.marbles[globals.summoners[b].curMarble].level
        rules.setLvl(globals.summoners[b].curMarble, rules.marbles[globals.summoners[a].curMarble].level)
        rules.setLvl(globals.summoners[a].curMarble, temp)

def changeRoles(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    b = args[1] if len(args) > 1 else None
    a = a[0].upper() + a[1:].lower()
    b = b[0].upper() + b[1:].lower()
    role1 = rules.marbles[globals.summoners[a].curMarble].position
    role2 = rules.marbles[globals.summoners[b].curMarble].position
    rules.changeRole(globals.summoners[b].curMarble, role1)
    rules.changeRole(globals.summoners[a].curMarble, role2)

def freedomRoleSteal(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    if a != rules.marbles[globals.summoners[lastSpinner].curMarble].position:
        rules.forceTakeRole(lastSpinner, a)
    
    rules.changeLetter(globals.summoners[lastSpinner].curMarble, "")

def marbleDec(args):
    if rules.godScenario:
        return
    victims = rules.getNoLetters()
    changeLetter(victims, isRandom=True)

def marbleLargeDec(args):
    if rules.godScenario:
        return
    a = args[0] if len(args) > 0 else None
    a = a[0].upper() + a[1:].lower()
    rules.forceNextLvl1(a)

def marbleInc(args):
    if rules.godScenario:
        return
    # a = args[0] if len(args) > 0 else None
    # b = args[1] if len(args) > 1 else None
    oldLvl = rules.marbles[globals.summoners[lastSpinner].curMarble].level
    print("Previous marble level: " + oldLvl)
    if oldLvl == "1":
        rules.setLvl(globals.summoners[lastSpinner].curMarble, "2")
        freedomRoleSteal(args)
    elif oldLvl == "2":
        rules.setLvl(globals.summoners[lastSpinner].curMarble, "3")
        marbleLargeInc(args)
    elif oldLvl == "3" or oldLvl == "4":
        message = lastSpinner + " has become MARBLE GOD!"
        print(rules.GREEN_TXT_START + message + rules.DEF_TXT_END)
        rules.assignMarblePlaceholders(message)
        rules.godScenario = True

def marbleLargeInc(args):
    if rules.godScenario:
        return
    rules.changeLetter(globals.summoners[lastSpinner].curMarble, "")

def nop(args):
    pass

def marbleGod(args):
    rules.assignMarblePlaceholders(lastSpinner+" is MARBLE GOD")

def helpHomies(args):
    rules.assignMarblePlaceholders("Help the homies")

# ========================================== end of wrappers =====================================

wheel_map = {
    "Adam swaps with support and plays bard": adamSuppBard, # ok
    "Bankrupt someone of your choice": bankruptPerson,
    "Change the letter for someone's Lvl1 Marble": changeLvl1Letter, # ok
    "Force two people with letters to trade letters (roles stay the same)": changeLetters, # ok
    "Force two people to trade roles (letters stay the same)": changeRoles,
    "Freedom (can boot someone off role and they take next same lvl marble for available role.)": freedomRoleSteal, # ok
    "JON & ADAM SHOT NOW": nop,
    "MARBLE GOD": marbleGod,
    "Marble - add random letter restriction to someone without one": marbleDec,
    "Marble -- force someone onto their next lvl1 marble of current role": marbleLargeDec, # ok
    "Marble + (1->2 can boot people off of role, 2->LETTER FREEDOM, 3 or 4->MARBLE GOD, 0->nothing)": marbleInc, # ok
    "Marble ++ (LETTER FREEDOM, roles don't change)": marbleLargeInc, # ok
    "raguyamotha swaps marbles with bot and has to play an actual ADC": rageBot, # ok
    "SCRAP MARBLES THE HOMIES NEED HELP": helpHomies,
    "Swap the money of two people": swapMoney,
    "Take $50 away from someone and keep it (can put them negative)": take50Dollars, # ok
    "Top lane trades marble with Kay": kayTop #ok
}

# max 2 inputs, possibility being summoner, letter, or role
wheel_map_inputs = {
    "Adam swaps with support and plays bard": ("", ""),
    "Bankrupt someone of your choice": ("summoner", ""),
    "Change the letter for someone's Lvl1 Marble": ("summonerLvl1", "letter"),
    "Force two people with letters to trade letters (roles stay the same)": ("summonerLetter", "summonerLetter"),
    "Force two people to trade roles (letters stay the same)": ("summoner", "summoner"),
    "Freedom (can boot someone off role and they take next same lvl marble for available role.)": ("role", ""),
    "JON & ADAM SHOT NOW": ("", ""),
    "MARBLE GOD": ("", ""),
    "Marble - add random letter restriction to someone without one": ("summonerNoLetter", ""),
    "Marble -- force someone onto their next lvl1 marble of current role": ("summoner", ""),
    "Marble + (1->2 can boot people off of role, 2->LETTER FREEDOM, 3 or 4->MARBLE GOD, 0->nothing)": ("role+", ""),
    "Marble ++ (LETTER FREEDOM, roles don't change)": ("", ""),
    "raguyamotha swaps marbles with bot and has to play an actual ADC": ("", ""),
    "SCRAP MARBLES THE HOMIES NEED HELP": ("", ""),
    "Swap the money of two people": ("summoner", "summoner"),
    "Take $50 away from someone and keep it (can put them negative)": ("summoner", ""),
    "Top lane trades marble with Kay": ("", "")
}