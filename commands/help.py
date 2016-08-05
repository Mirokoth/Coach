import asyncio

class Help():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command received
    async def on_message(self, message, command, arguments):
        res = 'This is a help file?\nCommand was {} and arguments {}'.format(command, arguments);
        return await self.coach.forward_message(message.channel, res)
