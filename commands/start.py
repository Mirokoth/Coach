import challonge
from config import config

# Command: Start a tournament
class Start():

    def __init__(self, message_handler, coach):
        self.command = "start"
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Start a tournament.".format(config.BOT_CMD_SYMBOL, self.command)
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        # await self.coach.forward_message(message.channel, "Please add the ID of the tournament you wish to see. ie. If the URL is **http://challonge.com/test** then type **'{}{} test**'".format(config.BOT_CMD_SYMBOL, command.lower()))

        if arguments == False:
            print('no arguments')
            # tournaments = challonge.tournaments.index()
            # # Verify null response
            # if len(tournaments) > 0:
            output = "Here's a list of pending tournaments:```"
            for tournament in challonge.tournaments.index():
                # check for state = pending?
                output += "{} (http://challonge.com/{})\n".format(tournament["name"], tournament["name"])
            output += "```"
            await self.coach.forward_message(message.channel, output)
                # output += "\nWarning: You are about to start the **{}** tournament. Are you sure? (yes or no)".format(tournament["name"])

            # tournament = challonge.tournaments.show(arguments[0])
            # await self.coach.forward_message(message.channel, "***Tournament details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))

        # else:
        #     try:
        #         tournament = challonge.tournaments.show(arguments[0])
