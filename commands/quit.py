import asyncio
from importlib import import_module

class Quit():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command received
    async def on_message(self, message, command, arguments):
        quote = import_module('modules.quote')
        await self.coach.forward_message(message.channel, '{}'.format(quote.getQuote()))
        quit()
