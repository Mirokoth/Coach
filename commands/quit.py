import asyncio
from coach import coach
from importlib import import_module

class message():
    async def __new__(self, message, command, arguments):
        random = import_module('commands.quote')
        #print(random.message.message())
        await coach.forward_message(message.channel, '{}'.format(random.message.message()))
        quit()
