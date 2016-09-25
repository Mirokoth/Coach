import challonge
from config import config

# Command: Start a tournament
class Start():

    def __init__(self, message_handler, coach):
        self.command = "start"
        self.adminRequired = True
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Start a specified tournament."
        return description

    async def on_message(self, message, command, arguments):
        tournaments = challonge.tournaments.index()

        # No tournament specified
        if arguments == False:

            # No pending tournaments
            if len(tournaments) == 0:
                res = "No tournaments pending."
                await self.coach.forward_message(message.channel, res)

            # There are pending tournaments
            else:
                # Return a list of pending tournaments
                output = "Choose a tournament to start - here's a list of pending tournaments:```"
                for tournament in tournaments:
                    if tournament["state"] == "pending":
                        output += "{} (http://challonge.com/{})\n".format(tournament["name"], tournament["name"])
                output += "```"
                await self.coach.forward_message(message.channel, output)

        # Check if the tournament provided is valid
        else:
            exists = False
            pending = False
            for tournament in tournaments:
                if tournament["name"].upper() == arguments[0].upper():
                    exists = True
                    if tournament["state"] == "pending":
                        pending = True

            print(exists, pending, tournament["name"])

            # Tournament is valid
            if exists == True and pending == True:
                # output += "\nWarning: You are about to start the **{}** tournament. Are you sure? (yes or no)".format(tournament["name"])
                await self.coach.forward_message(message.channel, "Starting!")

            # Tournament doesn't exist
            elif exists == False:
                await self.coach.forward_message(message.channel, "That tournament doesn't exist!")
            # Tournament already started
            elif pending == False:
                await self.coach.forward_message(message.channel, "That tournament has already started!")
