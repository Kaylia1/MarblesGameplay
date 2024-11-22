import json
import os
import time
import copy
import backendTools.webtools as webtools
import backendTools.globals as globals
import backendTools.rules as rules
import backendTools.wheelMap as wheelMap
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

def map_to_json(local_summoners):
    return {name: summoner_to_json(summoner) for name, summoner in local_summoners.items()}

# def save_state(json_data):
    # print("Writing to file")
    # with open("saved_points.json", "w") as file:
    #     json.dump(json_data, file, indent=4)
    # print("Points written to saved_points.json")

def load_state(json_data):
    # print("Loading from file")
    # if not os.path.exists("saved_points.json"):
    #     print("Could not open file, no data loaded (new session)?")
    #     return

    # with open("saved_points.json", "r") as file:
    #     json_data = json.load(file)

    for name, data in json_data.items():
        if name in globals.summoners:
            summoner = globals.summoners[name]
            summoner.money = data["money"]
            summoner.kills = data["kills"]
            summoner.deaths = data["deaths"]
            summoner.assists = data["assists"]

    print("Loaded from data.")

def scoreAdjust():
    playerData, isWin = webtools.getRiotAPIData()
        
    for summoner in globals.summoners.values():
        kills = playerData[summoner.name]["kills"]
        deaths = playerData[summoner.name]["deaths"]
        assists = playerData[summoner.name]["assists"]
        vision = playerData[summoner.name]["vision"]
        isSupp = playerData[summoner.name]["position"] == "SUPPORT"

        if isWin:
            summoner.money += 30

        if(isSupp):
            kills, assists = assists, kills
        summoner.kills += kills
        summoner.deaths += deaths
        summoner.assists += assists
        summoner.money += kills * KILLVALUE - deaths * DEATHVALUE + assists * ASSISTVALUE
        if(vision < 15):
            summoner.money -= 15
        elif(vision > 20):
            summoner.money += vision - 20
    
    print_money()
    return playerData # return for display