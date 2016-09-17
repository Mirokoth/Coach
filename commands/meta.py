import challonge
from config import config

# Command: Return high level details about a specific tournament
class Meta():
    def __init__(self, message_handler, coach):
        self.command = "meta"
        self.adminRequired = False
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "See high-level details about a specific tournament. ie. For  http://challonge.com/testtournament type '{}{} test'".format(config.BOT_CMD_SYMBOL, self.command)
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        if arguments == False:
            await self.coach.forward_message(message.channel, "Please add the ID of the tournament you wish to see. ie. If the URL is **http://challonge.com/test** then type **'{}{} test**'".format(config.BOT_CMD_SYMBOL, command.lower()))
        else:
            tournament = challonge.tournaments.show(arguments[0])
            await self.coach.forward_message(message.channel, "***Tournament details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))
