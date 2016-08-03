### ------------------------------------------------
###  All of the below infomation should remain
###  You can add any modules or code required
###m  message.channel and the string to send can be changed.
### ------------------------------------------------

# python modules
import asyncio
import os

# third-party modules
import challonge

# custom modules
from coach import coach
from config import config


DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL

class message():
    async def __new__(self, message, command, arguments):
        if arguments == False:
            await coach.forward_message(message.channel, "Please add the ID of the tournament you wish to see. ie. If the URL is **http://challonge.com/test** then type **'{}{} test**'".format(BOT_CMD_SYMBOL, command.lower()))
        else:
            tournament = challonge.tournaments.show(arguments[0])
            await coach.forward_message(message.channel, "***Tournament details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))
