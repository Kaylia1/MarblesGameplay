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
        print(data)

        # data is in format champName | role | winrate | numMatches

        key = tuple(data[:2])
        winrates[key] = {
            "winrate": data[2],
            "matches": data[3]
        }
    
    with open("./data/champList.txt", 'r') as file:
        lines = file.readlines()
        allChamps = [line.strip() for line in lines]

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
    print(allChamps[start_index][0])
    if start_index < len(allChamps) and allChamps[start_index][0].lower() == char:
        return start_index, end_index
    else:
        return -1, -1  # Character not found


def showStats(letter, role):
    # note currently marbles only supports one-character letter cause of this, though rules.py should support multi-char letters
    # letter can also be len 0 or ADC/BARD due to messiness
    if(len(letter) != 1):
        return

constructWinrates()
print(findChamp("A"))