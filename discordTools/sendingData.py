import backendTools.globals as globals
import backendTools.rules as rules
import tkTools.uiWinrates as uiWinrates
import tkTools.tkWheelPage as tkWheelPage

def align_columns(data):
    """Aligns columns with appropriate padding."""
    column_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]
    
    # Format the table into a string with code block formatting
    table_str = "```"  # Start a code block
    for row in data:
        formatted_row = ""
        for i, item in enumerate(row):
            formatted_row += f"{str(item):<{column_lengths[i]}}    "  # Add extra space for separation
        table_str += "\n" + formatted_row.strip()  # Add row to the table
    table_str += "\n```"  # End the code block
    return table_str

async def send_help_info(channel):
    header_data = [
                   ["Command", "Description"],
                   ["!help", "List all public commands"],
                   ["!isAlive", "Hello World! I am alive"],
                   ["!history", "Show cumulative money and kda"],
                   ["!money", "Show current money"],
                   ["!assignments", "Show current marble assignments"],
                   ["!wheel", "Show last wheel result"],
                   ["!vision", "Show summoner with best adjusted vision last game"],
                   ["!champstats <PlayerName>", "Show all possible winrates for that PlayerName's letter and role"],
                   ["!drink", "Show random quote about drinking"],
                   ["!top", "Show random quote disparaging top lane"],
                   ]
    info = align_columns(header_data)
    await channel.send(info)

async def send_summoner_data(channel):
    """Send summoner data to the specified channel."""
    # Headers
    headers = ["Name", "Money", "Kills", "Deaths", "Assists"]
    
    summonerData = [headers]
    
    # Iterate through summoners and their stats
    for key, summoner in globals.summoners.items():
        # Format summoner data as a string
        summonerData.append([key, summoner.money, summoner.kills, summoner.deaths, summoner.assists])   #f"{key} | ${summoner.money} | {summoner.kills} | {summoner.deaths} | {summoner.assists}")

    aligned_data = align_columns(summonerData)
    await channel.send(aligned_data)

async def send_money_data(channel):
    """Send summoner money data to the specified channel in table format."""
    headers = ["Name", "Money"]
    money_data = [headers]
    
    # Iterate through summoners and their money stats
    for key, summoner in globals.summoners.items():
        # Add summoner's money data to the list
        money_data.append([key, summoner.money])
    
    # Format the data into an aligned table string
    aligned_data = align_columns(money_data)
    await channel.send(aligned_data)

async def send_assignment_data(channel):
    """Send the assignment data in table format."""
    print(rules.marblesExist)
    if not rules.marblesExist:
        await channel.send("Marbles have not been assigned yet!")
        return

    # Headers for the table
    headers = ["Name", "Position", "Letter", "Level"]
    assignment_data = [headers]

    # Iterate through summoners and their stats
    for key, summoner in globals.summoners.items():
        marble = rules.marbles[summoner.curMarble]
        assignment_data.append([key, marble.position, marble.letter, marble.level])
    
    aligned_data = align_columns(assignment_data)
    await channel.send(aligned_data)

async def send_wheel_res_data(channel):
    await channel.send("Last wheel spin: "+tkWheelPage.wheel_result)

async def send_winrate_data(channel, summonerName):
    """Send the assignment data in table format."""
    if uiWinrates.Winrates.appData == None:
        await channel.send("Winrates are not known yet!")
        return
    elif summonerName not in globals.allSummoners:
        await channel.send("Bad summoner name input")
        return

    # Headers for the table
    headers = ["Champ", "Winrate", "Matches"]
    winrate_data = [headers]
    
    i = globals.allSummoners.index(summonerName) # TODO case sensitive
    data = uiWinrates.Winrates.appData[i]
    for i, (champ, winrate, matches) in enumerate(data):
        winrate_data.append([champ, winrate, matches])
    
    aligned_data = align_columns(winrate_data)
    await channel.send(aligned_data)