import asyncio
from coach import coach

class message():
    async def __new__(self, message, command, arguments):
        await coach.forward_message(message.channel, 'This is a help file?\nCommand was {} and arguments {}'.format(command, arguments))
