# python modules
import asyncio
# third-party modules
import discord
# custom modules
from modules.message_handler import message_handler
# config
from config import config

client = discord.Client()
server_list = []

# --------------
# Discord Events
# --------------

class coach():

    # Bot Ready
    @client.event
    async def on_ready():
        # Log some startup information
        print('Logged in as {} ({}) with the following connected servers..'.format(client.user.name, client.user.id))
        print('------')
        for server in client.servers:
            print('{} ({})'.format(server.name, server.id))
        # Cache server list
        for server in client.servers:
            server_list.append(server)
        print('------')
        print('Get this guy a jockstrap and a cookie!')
        print('------')
        print('Bot user ID: {}'.format(client.user.id))

    # Message Received
    @client.event
    async def on_message(message):
        if message.author.id != client.user.id:
            # Send command to message_handler for processing
            asyncio.ensure_future(message_handler.the_message(message))

    # Forwards received arguments to chat
    async def forward_message(*args, **kwargs):
        return await client.send_message(*args, **kwargs)

client.run(config.BOT_TOKEN)
