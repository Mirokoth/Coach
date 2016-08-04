import asyncio
# from coach import Coach

class Help():
    def __init__(self, coach):
        self.coach = coach
    async def test(self, message, command, arguments):    
        res = 'This is a help file?\nCommand was {} and arguments {}'.format(command, arguments);
        return await self.coach.forward_message(message.channel, res)
