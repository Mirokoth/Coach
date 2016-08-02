# modules
import asyncio
import json
import os
from proc_message import proc_message

# third-party modules
import discord
import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# config
import config

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
client = discord.Client()
roles = []
server_lst = []

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
# Log the number of tournaments found
print("{} tournaments found under this account.".format(len(challonge.tournaments.index())))

print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
print(tournament["started-at"]) # None

# --------------
# Discord Events
# --------------
class coach(discord.Client):
    # Bot Ready
    @client.event
    async def on_ready():
        print('Logged in as {} ({}) with the following connected servers..'.format(client.user.name, client.user.id))
        print('------')
        for server in client.servers:
            print('{} ({})'.format(server.name, server.id))
        # Cache server list
        for server in client.servers:
            server_lst.append(server)
        print('------')
        print('Get this guy a jockstrap and a cookie!')
        print('------')

    # Message Received
    @client.event

    async def on_message(message):
        asyncio.ensure_future(proc_message.the_message(message))

    async def send_message(self, *args, **kwargs):
        return await super().send_message(*args, **kwargs)
