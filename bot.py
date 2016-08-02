from coach import coach
import os
import discord
import config
import asyncio

# --- CONFIG ---

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
client = discord.Client()
roles = []
server_lst = []
client = coach()
BOT_TOKEN = config.BOT_TOKEN
# --- RUN BOT ---

coach.run(BOT_TOKEN)
