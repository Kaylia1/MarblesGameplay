# bot.py
import os

import discord
from dotenv import load_dotenv

import tkTools.tkUtil as tkUtil
import tkTools.tkHomePage as tkHomePage, tkTools.tkPostgamePage as tkPostgamePage
import tkTools.tkPickingPage as tkPickingPage, tkTools.tkAdjustmentsPage as tkAdjustmentsPage
import backendTools.parseChampStats as parseChampStats
import tkTools.tkWheelPage as tkWheelPage
import tkTools.tkWheelResultPage as tkWheelResultPage
import tkTools.tkMidgamePage as tkMidgamePage
import tkTools.tkUtil as tkUtil
import tkinter as tk
import backendTools.points as points
import backendTools.globals as globals
import discordTools.sendingData as sendingData
import firebase.firebaseTools as firebaseTools
import threading
import data.dumbPosts.alcoholQuotes as alcoholQuotes
import data.dumbPosts.toplaneQuotes as toplaneQuotes
import random


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

parseChampStats.constructWinrates()


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
    elif message.content.startswith('!winrate'):
        if len(message.content.split(" "))>1:
            await sendingData.send_winrate_data(message.channel, message.content.split(" ")[1])
    
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
    client.run(TOKEN)

# Run the bot in a separate thread
# TODO ton of race conditions, but since these are all read operations maybe we don't care?
discord_thread = threading.Thread(target=start_discord_bot, daemon=True)
discord_thread.start()