from importlib import import_module

# Command: Send some final words and restart the bot
class Quit():

    def __init__(self, message_handler, coach):
        self.command = "quit"
        self.adminRequired = True
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Quit and sometimes restart"
        return description

    async def on_message(self, message, command, arguments):
        # Send a random quote
        quote = import_module('modules.quote').getQuote()
        await self.coach.forward_message(message.channel, '{}'.format(quote))
        # Quit
        quit()
