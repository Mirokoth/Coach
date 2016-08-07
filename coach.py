# python modules
import asyncio
# third-party modules
import discord
# custom modules
from modules.message_handler import message_handler
# config
from config import config
server_list = []

'''
Inherit and override the discord.Client class
Distribute behaviour to other modules from here
'''
class Coach(discord.Client):

    # There is no __init__ here as when overriding this default behaviour we get a few errors

    # Bot Ready
    async def on_ready(self):
        # Log some startup information
        print('Logged in as {} ({}) with the following connected servers..'.format(self.user.name, self.user.id))
        print('------')
        for server in self.servers:
            print('{} ({})'.format(server.name, server.id))
        # Cache server list
        for server in self.servers:
            server_list.append(server)
        print('------')
        print('Get this guy a jockstrap and a cookie!')
        print('------')
        print('Bot user ID: {}'.format(self.user.id))

    # Send message to handler
    async def forward_message(self, *args, **kwargs):
        return await self.send_message(*args, **kwargs)

    # Message Received
    async def on_message(self, message):
        if message.author.id != self.user.id:
            # Send command to message_handler for processing
            # asyncio.ensure_future(self.message_handler.the_message(message))
            # loop = asyncio.get_event_loop()

            # Instantiate message handler
            # TODO: Move this to __init__
            self.message_handler = message_handler(self)

            # Pass message to the message handler
            self.loop.create_task(self.message_handler.the_message(message))

coach = Coach().run(config.BOT_TOKEN)
