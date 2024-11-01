import bisect

# parse the pre-generated winrates scraped from u gg

winrates = {}
allChamps = []

def constructWinrates():
    global allChamps, winrates
    alldata = []
    with open("./data/winrates.txt", 'r') as file:
        alldata = file.readlines()
        alldata = [line.strip() for line in alldata]
    
    for data in alldata:
        data = data.split()
        # data is in format champName | role | winrate | numMatches
        key = tuple(data[:2])
        winrates[key] = {
            "winrate": data[2],
            "matches": data[3]
        }
    
    with open("./data/champList.txt", 'r') as file:
        lines = file.readlines()
        allChamps = []
        for line in lines:
            if(line.strip() != ""):
                allChamps.append(line.strip())

def getChamps(char, role):
    if(len(char) != 1):
        return []
    
    start, end = findChamp(char)
    selectedChamps = allChamps[start:end+1]
    result = []
    for champ in selectedChamps:
        result.append((champ, role))
    return result

# for optimization, binary search for champs that start with that letter (try to make this extendable to substr)
# returns first and last indices of list
# TODO do this properly lmao
def findChamp(char):
    char = char.lower()
    
    # Find the index of the first string starting with the given character
    start_index = bisect.bisect_left(allChamps, char)

    # Find the index of the first string starting with the next character
    next_char = chr(ord(char) + 1)  # Increment character
    end_index = bisect.bisect_left(allChamps, next_char) - 1

    # Adjust start_index if it's out of bounds or doesn't match
    if start_index < len(allChamps) and allChamps[start_index][0].lower() == char:
        return start_index, end_index
    else:
        return -1, -1  # Character not found