import json
import os
import time
import copy
import webtools
import globals
import rules

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

def save_state(json_data):
    print("Writing to file")
    with open("saved_points.json", "w") as file:
        json.dump(json_data, file, indent=4)
    print("Points written to saved_points.json")

def load_state():
    print("Loading from file")
    if not os.path.exists("saved_points.json"):
        print("Could not open file, no data loaded (new session)?")
        return

    with open("saved_points.json", "r") as file:
        json_data = json.load(file)

    for name, data in json_data.items():
        if name in globals.summoners:
            summoner = globals.summoners[name]
            summoner.money = data["money"]
            summoner.kills = data["kills"]
            summoner.deaths = data["deaths"]
            summoner.assists = data["assists"]

    print("Loaded from file.")

def main():
    print("Enter negative number to quit and display stats.")
    print()

    load_state()
    
    rules.assignMarbles()

    while True:
        win = input("Win? (Y/N): ").strip().lower()

        if win == 'y':
            for summoner in globals.summoners.values():
                summoner.money += 30

        webtools.updateOPGG()
        playerData = webtools.getRiotData()
        ok = input("Ok? Y=continue, N=cancel riot data, manually input match data instead").strip().lower()
        for summoner in globals.summoners.values():
            if(ok):
                kills = playerData[summoner.gameName]["kills"]
                deaths = playerData[summoner.gameName]["deaths"]
                assists = playerData[summoner.gameName]["assists"]
                vision = playerData[summoner.gameName]["vision"]
                isSupp = playerData[summoner.gameName]["position"] == "SUPPORT"
            else: 
                while True:
                    try:
                        kills, deaths, assists, isSupp, vision = map(int, input(f"Enter {summoner.name}'s kills, deaths, assists, isSupport, vision: ").split())
                        if kills < 0 or deaths < 0 or assists < 0 or (isSupp not in (0, 1)) or vision < 0:
                            close()
                            return
                        break
                    except ValueError:
                        print("Dumbass. Enter integers please.")
                        print()

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
            
        
        while True:
            print()
            print_money()
            
            action = input("Action? B=bribe, W=wheel, C=continue").strip().lower()
            if(action == "c"):
                break
            elif(action == "b"):
                name, name2, amount = input("From who? To who? How much? ").split()
                amount = int(amount)

                if name not in globals.summoners or name2 not in globals.summoners:
                    print("Dumbass. Enter someone's name. Type it correctly. (name) (name) (amount)")
                    continue

                send = globals.summoners[name]
                receive = globals.summoners[name2]

                send.money -= amount
                receive.money += amount

                print(f"{send.name} now has: ${send.money}")
                print(f"{receive.name} now has: ${receive.money}")
                print()
            elif(action == "w"):
                name = input("Who? ").strip()
                if name not in globals.summoners:
                    print("Dumbass. Enter someone's name. Type it correctly.")
                    continue

                summoner = globals.summoners[name]
                if summoner.money >= 100:
                    summoner.money -= 100
                    print(f"{summoner.name} now has: ${summoner.money}")
                else:
                    print(f"{name} cannot afford to spin the wheel.")
                print()

        # Save state at end of each game
        output = map_to_json(globals.summoners)
        save_state(output)

if __name__ == "__main__":
    main()
