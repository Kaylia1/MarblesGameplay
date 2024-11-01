import requests
import re

data = requests.get("https://www.leagueoflegends.com/en-us/champions/")
text = data.content.decode("utf-8")

substring = "\"card-title\">"

results = []
start = 0

while True:
    # Find the next occurrence of the substring
    substring_start = text.find(substring, start)
    
    # If no more occurrences are found, break the loop
    if substring_start == -1:
        break
    
    # Calculate the start of the content after the substring
    content_start = substring_start + len(substring)
    
    # Find the next '<' character after the substring
    next_char_index = text.find('<', content_start)
    
    # Extract the content up to the next '<' character
    if next_char_index != -1:
        extracted = text[content_start:next_char_index]
    else:
        # If no '<' is found, extract to the end of the text
        extracted = text[content_start:]
    
    print(extracted.strip())
    
    # Strip any whitespace or leading/trailing newlines and add to results
    results.append(extracted.strip())
    
    # Move start to the end of the current occurrence
    start = content_start

with open("../data/champList.txt", "w") as f:
    for i, item in enumerate(results):
        # Remove non-alphabetic characters, make lowercase, and replace spaces with underscores
        processed_item = re.sub(r'[^a-zA-Z\s]', '', item.replace('&#x27;', "")).lower().replace(' ', '_')
        
        if processed_item == "nunu_amp_willump":
            processed_item = "nunu"
        elif processed_item == "renata_glasc":
            processed_item = "renata"
        
        if(i==len(results)-1):
            f.write(processed_item)
        else:
            f.write(processed_item + "\n")