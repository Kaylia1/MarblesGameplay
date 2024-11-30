# bot.py
import os

import discord
from dotenv import load_dotenv

import uiTools.uiPage as uiPage
import uiTools.uiHomePage as uiHomePage, uiTools.uiPostgamePage as uiPostgamePage
import uiTools.uiPickingPage as uiPickingPage, uiTools.uiAdjustmentsPage as uiAdjustmentsPage
import backendTools.parseChampStats as parseChampStats
import uiTools.uiWheelPage as uiWheelPage
import uiTools.uiWheelResultPage as uiWheelResultPage
import uiTools.uiMidgamePage as uiMidgamePage
import uiTools.uiPage as uiPage
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import discordTools.sendingData as sendingData
import firebase.firebaseTools as firebaseTools
import threading
import data.dumbPosts.alcoholQuotes as alcoholQuotes
import data.dumbPosts.toplaneQuotes as toplaneQuotes
import random
import backendTools.rules as rules
import time

load_dotenv(dotenv_path="secrets/.env")
readingMarbles = False
TOKEN = os.getenv('DISCORD_TOKEN') # if you are not Kaylia then you can't run this

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)
parseChampStats.constructWinrates() # Only necessary if not run alongside tkGUI.py

startTime = 0

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    global readingMarbles
    # Make sure the bot doesn't reply to its own messages
    if message.author == client.user:
        return

    print(f'Message sent by {message.author.name}: {message.content}')

    # Respond to text messages
    if message.content.startswith('!isAlive'):
        await message.channel.send('Hello World! I am alive')
    elif message.content.startswith('!help'):
        await sendingData.send_help_info(message.channel)
    elif message.content.startswith('!games'):
        await message.channel.send('Total games played:'+str(globals.totalGames))
    elif message.content.startswith('!history'):
        points.load_state(firebaseTools.fb.loadData())
        await sendingData.send_summoner_data(message.channel)
    elif message.content.startswith('!money'):
        await sendingData.send_money_data(message.channel)
    elif message.content.startswith('!drink'):
        random_index = random.randint(0, len(alcoholQuotes.quotes) - 1)
        await message.channel.send(alcoholQuotes.quotes[random_index])
    elif message.content.startswith('!top'):
        random_index = random.randint(0, len(toplaneQuotes.quotes) - 1)
        await message.channel.send(toplaneQuotes.quotes[random_index])
    elif message.content.startswith('!assignments'):
        await sendingData.send_assignment_data(message.channel)
    elif message.content.startswith('!vision'):
        await message.channel.send("Summoner with the best adjusted vision last game was: "+rules.bestVision)
    elif message.content.startswith('!champstats'):
        if len(message.content.split(" "))>1:
            await sendingData.send_winrate_data(message.channel, message.content.split(" ")[1])
    elif message.content.startswith('!stats'):
        await sendingData.send_stats(message.channel)
    elif message.content.startswith('!wheel'):
        await sendingData.send_wheel_res_data(message.channel)
    elif message.author.name == "smolfroggo":
        if message.content.startswith('!page'):
            await message.channel.send(uiPage.getCurPage())
        elif message.content.startswith('!runtime'):
            global startTime
            endTime = time.time()
            hours, rem = divmod(endTime - startTime, 3600)
            minutes, seconds = divmod(rem, 60)
            await message.channel.send(f"Elapsed time: {int(hours):02}:{int(minutes):02}:{seconds:.2f}")
        elif message.content.startswith('!updatehash'):
            file_path = "local_commit_hash.txt"
            if os.path.exists(file_path):
                # Open the file and read its contents
                with open(file_path, 'r') as file:
                    contents = file.read()
                await message.channel.send(contents)
            else:
                await message.channel.send("No hash")
        
    
    # do we want to support overriding the UI with the bot?
    # if client.user.mention in message.content:
    #     if "marbles" in message.content.lower():
    #         readingMarbles = True
    #         await message.channel.send("Listening! Paste marbles")

    # # Read uploaded marbles data
    # if readingMarbles and message.attachments:
    #     for attachment in message.attachments:
    #         # Read the file content
    #         file_content = await attachment.read()

    #         # If the file is a text file, decode and print its content
    #         try:
    #             file_text = file_content.decode('utf-8')  # Decode the content to a string
    #             readingMarbles = False
    #             await message.channel.send("Finished reading marbles data")
    #             # await message.channel.send(f"Here's the content of {attachment.filename}: \n{file_text}")
    #         except UnicodeDecodeError:
    #             print(f"Cannot decode {attachment.filename}, it's not a text file.")
    #             await message.channel.send(f"Sorry, I can't read {attachment.filename}, it's not a text file.")

def start_discord_bot():
    """Function to start the Discord bot."""
    global startTime
    startTime = time.time()
    client.run(TOKEN)

# Run the bot in a separate thread
# TODO ton of race conditions, but since these are all read operations maybe we don't care?
discord_thread = threading.Thread(target=start_discord_bot, daemon=True)
discord_thread.start()