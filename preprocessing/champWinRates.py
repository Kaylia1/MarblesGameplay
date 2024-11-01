# Preprocess champion win rates and save to file in data folder
# import requests

# result = requests.get("https://u.gg/lol/champions/veigar/build/jungle")

# print(result.content)

import urllib.request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import globals


search_string = "</div><div class=\"label\">Win Rate"
match_substr = "matches\"><div class=\"value\">"


# find percentage win rate as string with percentage sign and numMatches as string
def getWinRate(champ, position):
    # note: cloudflare blocks unauthorized data scraping, but urllib gets around it somehow
    req = urllib.request.Request("https://u.gg/lol/champions/"+champ+"/build/"+position)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')

    r = urllib.request.urlopen(req).read()
    r = r.decode('utf-8')

    substring_start = r.find(search_string)
    # Find the last occurrence of '>' before the substring
    last_greater_than = r.rfind(">", 0, substring_start)
    
    # parse number of matches
    substring_start2 = r.find(match_substr)
    content_start = substring_start2 + len(match_substr)
    # Find the next '<' character after the substring
    next_char_index = r.find('<', content_start)

    return r[last_greater_than + 1:substring_start], r[content_start:next_char_index]


champs = []
with open("../data/champList.txt", 'r') as file:
    champs = file.readlines()
    champs = [line.strip() for line in champs]

with open("../data/winrates.txt", 'w+') as file:
    for champ in champs:
        for role in globals.ROLES:
            winRateStr, matches = getWinRate(champ, role)
            file.write(champ+" "+role+" "+winRateStr+" "+matches+"\n")