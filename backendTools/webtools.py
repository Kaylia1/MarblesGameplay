
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the webdriver (replace with your browser)
# disable certificate checking, good thing this code is not industry-standard

def updateOPGG():
    options = Options()
    options.headless = False
    # ChromeDriver is just AWFUL because every version or two it breaks unless you pass cryptic arguments
    # AGRESSIVE: options.setPageLoadStrategy(PageLoadStrategy.NONE) # https://www.skptricks.com/2018/08/timed-out-receiving-message-from-renderer-selenium.html
    options.add_argument("start-maximized") # https://stackoverflow.com/a/26283818/1689770
    options.add_argument("enable-automation") # https://stackoverflow.com/a/43840128/1689770
    options.add_argument("--no-sandbox") #https://stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-dev-shm-usage") #https://stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-browser-side-navigation") #https://stackoverflow.com/a/49123152/1689770
    options.add_argument("--disable-gpu") #https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

    # er my own research which may be less accurate:
    # options.add_argument('--ignore-certificate-errors') # not sure why this doesn't make the warning disappear but it loads now
    # options.add_argument('--allow-insecure-localhost')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu') # otherwise skia issues
    # # I don't think these flags do anything btw
    # options.add_argument('--disable-web-security')  # Disables web security
    # options.add_argument('--allow-file-access-from-files')  # Allows access to files
    # options.add_argument('--start-maximized') # focuses window so that selenium can find button

    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        if elapsed_time > 60:  # Check if over 1 min passed
            print("Timeout exceeded, assumed you pushed it manually, exiting the loop.")
            break
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(5) # bruh idk why this works
        
        try:
            driver.get('https://www.op.gg/summoners/na/KayFish66-3435')
            
            # Bring the window to focus, idk if this does anything
            # driver.switch_to.window(driver.current_window_handle)
            
            button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span/span[text()='Update']]"))
            )
            button.click()

            # Close the browser
            break
        except Exception as e:
                print(f"Failed to push Update button: {str(e)}. Retrying...")
                time.sleep(1)
        finally:
            driver.quit()

    # uhhh for some reason making a seperate GET request works better than using the driver,
    # I suspect cause the webpage itself is korean and the korean characters make the unicode angry
    print("NOTE: If on Windows, any printed error messages above this should be ignored, it's not actually an error")
    
def getRiotData():
    print("Assuming update worked, making normal GET request")

    # Making a GET request
    r = requests.get('https://www.op.gg/summoners/na/KayFish66-3435')
    data = r.content # bytes object

    keyword = b"\"games\":{\"data\":["
    position = data.find(keyword)
    position += len(keyword)
    print("--------------")

    gameData = {}

    braces = 1
    failed = 1
    # find end of json for this game's data
    for i in range(position + 1, len(data)):
        if data[i:i+1] == b'{':
            braces += 1  # Found another opening brace
        elif data[i:i+1] == b'}':
            braces -= 1  # Found a closing brace
            # If stack is 0, we've matched all previous opening braces
            if braces == 0:
                failed = 0
                # print("found end at "+str(i))
                # print(data[position:i+1].decode("utf-8", errors="ignore"))    
                gameData = json.loads(data[position:i+1].decode("utf-8", errors="ignore"))
                break

    playerData = {}
    for summoner in gameData["participants"]:
        # this is hardcoded, should use summoners variable tbh
        if summoner["summoner"]["game_name"] == "Nobunagaa" or summoner["summoner"]["game_name"] == "KayFish66" or summoner["summoner"]["game_name"] == "reverie" or summoner["summoner"]["game_name"] == "lnanity" or summoner["summoner"]["game_name"] == "Jonpachiro":
            print("found "+summoner["summoner"]["game_name"]+"'s kda "+str(summoner["stats"]["kill"])+" "+str(summoner["stats"]["death"])+" "+str(summoner["stats"]["assist"])+" "+str(summoner["position"])+" vision:"+str(summoner["stats"]["vision_score"]))
            playerData[summoner["summoner"]["game_name"]] = {
                "kills": summoner["stats"]["kill"],
                "deaths": summoner["stats"]["death"],
                "assists": summoner["stats"]["assist"],
                "vision": summoner["stats"]["vision_score"],
                "position": summoner["position"]
            }
    
    team = gameData["myData"]["team_key"] # either RED or BLUE
    firstTeam = gameData["teams"][0]["key"]
    firstTeamWin = gameData["teams"][0]["game_stat"]["is_win"]
    ourWin = firstTeamWin if firstTeam == team else not firstTeamWin

    print("finish with status code "+str(failed))
    return playerData, ourWin