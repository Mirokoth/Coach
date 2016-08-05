import asyncio
from importlib import import_module

class Quit():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command received
    async def on_message(self, message, command, arguments):
        random = import_module('commands.quote')
        #print(random.message.message())
        await self.coach.forward_message(message.channel, '{}'.format(random.message.message()))
        quit()
