# python modules
import asyncio
import os

# third-party modules
import challonge

# custom modules
from config import config
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL

class Meta():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command description
    def get_description(self):
        description = "Wow so meta"
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        if arguments == False:
            await self.coach.forward_message(message.channel, "Please add the ID of the tournament you wish to see. ie. If the URL is **http://challonge.com/test** then type **'{}{} test**'".format(BOT_CMD_SYMBOL, command.lower()))
        else:
            tournament = challonge.tournaments.show(arguments[0])
            await self.coach.forward_message(message.channel, "***Tournament details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))
