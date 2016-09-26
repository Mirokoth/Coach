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
        await self.coach.send_typing(message.channel)
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
                output = "Choose a tournament to start with **{}{} <tournament name>**. Here's a list of pending tournaments:```".format(config.BOT_CMD_SYMBOL, self.command)
                for tournament in tournaments:
                    if tournament["state"] == "pending":
                        output += "{} (http://challonge.com/{})\n".format(tournament["name"], tournament["name"])
                output += "```"
                await self.coach.forward_message(message.channel, output)

        # Check if the tournament provided is valid
        else:
            userId = message.author.id
            requested_confirmation = self.message_handler.commandInProgress(self.command, userId)

            # Confirmation was requested
            if requested_confirmation == True:

                # Received confirmation
                if arguments[0].upper() == "Y" or arguments[0].upper() == "YES":
                    await self.coach.forward_message(message.channel, "Starting..")
                    await self.coach.send_typing(message.channel)

                    # Grab the tournament from store
                    tournamentId = self.message_handler.getCommandState(self.command, userId)

                    # Start the tournament
                    try:
                        challonge.tournaments.start(tournamentId)
                    except challonge.api.ChallongeException as err:
                        await self.coach.forward_message(message.channel, err)
                    else:
                        await self.coach.forward_message(message.channel, "Shit went whack, dawg. Contact someone sustaining elevated levels of authorate'")

                    tournament = challonge.tournaments.show(tournamentId)

                    # Check tournament state
                    if tournament["state"] != "pending":
                        self.message_handler.resetCommandState(self.command, userId)
                        await self.coach.forward_message(message.channel, "Started **{}** successfully!".format(tournament["name"]))
                    else:
                        await self.coach.forward_message(message.channel, "Error starting {}!".format(tournament["name"]))

                # Discard request
                elif arguments[0].upper() == "N" or arguments[0].upper() == "NO":
                    self.message_handler.resetCommandState(self.command, userId)
                    await self.coach.forward_message(message.channel, "I never liked you anyway.")

                # Invalid confirmation
                else:
                    await self.coach.forward_message(message.channel, "..Yeah-nah?")

                # Clear request for confirmation
                self.message_handler.resetCommandState(self.command, userId)

            # Confirmation has not been requested yet
            else:
                exists = False
                pending = False
                for tournament in tournaments:
                    # Tournament exists
                    if tournament["name"].upper() == arguments[0].upper():
                        exists = True
                        # # Request confirmation
                        if tournament["state"] == "pending":
                            pending = True
                            # Store tournament ID
                            self.message_handler.setCommandState(self.command, userId, tournament["id"])
                            await self.coach.forward_message(message.channel, "You are about to start the **{}** tournament. Are you sure? (yes or no)".format(tournament["name"]))

                # Tournament doesn't exist
                if exists == False:
                    await self.coach.forward_message(message.channel, "That tournament doesn't exist!")

                # Tournament already started
                elif pending == False:
                    await self.coach.forward_message(message.channel, "That tournament has already started!")
