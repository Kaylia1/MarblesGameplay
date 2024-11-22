import requests
import json
import backendTools.globals as globals

key = "?api_key=RGAPI-7c8bbb45-bfb5-4866-bfdc-3b70725a5ecd"

r = requests.get("https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/KayFish66/3435"+key)
accountData = r.json()

puuid = accountData["puuid"]

# get matches
r = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"+key)
lastMatch = r.json()[0]
print(lastMatch)

r = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{lastMatch}"+key)

# print()
# print(puuid)
# print(r.json())
gameData = r.json()
    
playerData = {}
isWin = False
for summoner in gameData["info"]["participants"]:
    # this is hardcoded, should use summoners variable tbh
    for name, appSummoner in globals.summoners.items():
        if summoner["riotIdGameName"] == appSummoner.gameName or summoner["riotIdGameName"] == appSummoner.altName:
            print("found "+name+"'s kda "+str(summoner["kills"])+" "+str(summoner["deaths"])+" "+str(summoner["assists"])+" "+str(summoner["lane"])+" vision:"+str(summoner["visionScore"]))
            # playerData maps in-game name to kda, pos
            playerData[summoner["riotIdGameName"]] = {
                "kills": summoner["kills"],
                "deaths": summoner["deaths"],
                "assists": summoner["assists"],
                "vision": summoner["visionScore"],
                "position": summoner["lane"]
            }
            isWin = summoner["win"]
print(playerData)
print(isWin)