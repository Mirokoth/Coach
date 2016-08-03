import asyncio
from coach import coach

class message():
    async def __new__(self, message, command, arguments):
        await coach.forward_message(message.channel, '{} - Not a recognised command'.format(message.content))
