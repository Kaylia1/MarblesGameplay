import tkinter as tk
class Summoner:
    def __init__(self, name, gameName, altName=""):
        self.name = name
        self.gameName = gameName
        self.altName = altName # if someone uses their alt account
        self.money = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.curMarble = 0

# Initialize summoners
summoners = {
    "Adam": Summoner("Adam", "lnanity"),
    "Rage": Summoner("Rage", "reverie", "TheHerbanLegends"),
    "Kaylia": Summoner("Kaylia", "KayFish66"),
    "Jon": Summoner("Jon", "Jonpachiro"),
    "Irisu": Summoner("Irisu", "Nobunagaa"),
}

allSummoners = ["Adam", "Rage", "Kaylia", "Jon", "Irisu"]
ROLES = ["jungle", "support", "top", "mid", "bot"]

totalGames = 0

mode = ""