class Summoner:
    def __init__(self, name, gameName):
        self.name = name
        self.gameName = gameName
        self.money = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.curMarble = 0

# Initialize summoners
summoners = {
    "Adam": Summoner("Adam", "lnanity"),
    "Rage": Summoner("Rage", "reverie"),
    "Kaylia": Summoner("Kaylia", "KayFish66"),
    "Jon": Summoner("Jon", "Jonpachiro"),
    "Irisu": Summoner("Irisu", "Nobunagaa"),
}

allSummoners = ["Adam", "Rage", "Kaylia", "Jon", "Irisu"]

def inputSummoner(validSummoners=allSummoners):
    while True:
        name = input("Who? ").strip()
        if name not in validSummoners:
            print("Dumbass. Enter someone's name. Type it correctly.")
            continue
        return name