import backendTools.globals as globals
import backendTools.rules as rules

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