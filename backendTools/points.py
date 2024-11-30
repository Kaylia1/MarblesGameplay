import json
import os
import time
import copy
import backendTools.webtools as webtools
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.wheelMap as wheelMap
import random
# import tkWheel
# import tkChampStats

KILLVALUE = 4
DEATHVALUE = 3
ASSISTVALUE = 1



def close():
    print()
    for summoner in globals.summoners.values():
        print(f"{summoner.name}'s stats:")
        print(f"Money: ${summoner.money}")
        print(f"Kills: {summoner.kills}")
        print(f"Deaths: {summoner.deaths}")
        print(f"Assists: {summoner.assists}")
        print()

def print_money():
    print()
    for summoner in globals.summoners.values():
        print(f"{summoner.name}'s money is: ${summoner.money}")
    print()

def summoner_to_json(summoner):
    return {
        "money": summoner.money,
        "kills": summoner.kills,
        "deaths": summoner.deaths,
        "assists": summoner.assists
    }

# construct fb data to store in cloud
def map_to_json(local_summoners):
    fbData = {name: summoner_to_json(summoner) for name, summoner in local_summoners.items()}
    fbData["special"] =  {"bestVision": rules.bestVision} # assume bestVision updated  in postgame properly
    fbData["overall"] = globals.totalGames
    return fbData

# read fb data
def load_state(json_data):
    for name, data in json_data.items():
        if name in globals.summoners:
            summoner = globals.summoners[name]
            summoner.money = data["money"]
            summoner.kills = data["kills"]
            summoner.deaths = data["deaths"]
            summoner.assists = data["assists"]
        elif name == "special":
            if "bestVision" in data:
                rules.bestVision = data["bestVision"]
        elif name == "overall":
            if "games" in data:
                globals.totalGames = data["games"]

    print("Loaded from data.")

def findSupp(playerData):
    lowestLaneCS = None
    highestJungCS = None
    support = None
    jungler = None

    for summoner in globals.summoners.values():
        jungCS = playerData[summoner.name]["jungleCsPre10"]
        laneCS = playerData[summoner.name]["csPre10"]

        if highestJungCS == None:
            highestJungCS = jungCS
            jungler = summoner.name
        elif lowestLaneCS == None:
            lowestLaneCS = laneCS
            support = summoner.name
        elif jungCS > highestJungCS:
            highestJungCS = jungCS
            jungler = summoner.name
        elif laneCS < lowestLaneCS:
            lowestLaneCS = laneCS
            support = summoner.name

    return support

def scoreAdjust():
    playerData, isWin = webtools.getRiotAPIData()
    support = findSupp(playerData)

    bestVisionScore = 0
    for summoner in globals.summoners.values():
        kills = playerData[summoner.name]["kills"]
        deaths = playerData[summoner.name]["deaths"]
        assists = playerData[summoner.name]["assists"]
        vision = playerData[summoner.name]["vision"]
        isSupp = support == summoner.name

        if isWin:
            summoner.money += 30

        summoner.kills += kills
        summoner.deaths += deaths
        summoner.assists += assists
        
        if(isSupp):
            vision *= 0.6 # supp needs 15/0.6=25 vision score to avoid penalty
            summoner.money += assists * KILLVALUE - deaths * DEATHVALUE + kills * ASSISTVALUE
        else:
            summoner.money += kills * KILLVALUE - deaths * DEATHVALUE + assists * ASSISTVALUE
        
        if(vision < 15):
            summoner.money -= 15
        elif(vision > 20):
            summoner.money += vision - 20
        
        # best adjusted vision or random tiebreak
        if vision > bestVisionScore or vision == bestVisionScore and random.randint(0, 1) == 0:
            rules.bestVision = summoner.name
            bestVisionScore = vision
    
    print_money()
    return playerData, support # return for display