import challonge

# Command: See all active tournaments and a huge list of all variables
class Details():
    def __init__(self, message_handler, coach):
        self.command = "details"
        self.adminRequired = True
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "See all active tournaments."
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        # Command: Send full responses for active tournaments associated to an account
        count = 0
        # Send details for each active tournament under this account
        for tournament in challonge.tournaments.index():
            count += 1
            output = "" # String to send
            # Start the message
            output += "\n**Tournament Details** for **{}**:\n ".format(tournament["name"])
            # Append each property in the tournament
            for prop in tournament:
                output += "{}: {}\n".format(prop, tournament[prop])
            # Tie up the message
            output += ""
            # Send all tournament details from Challonge response
            await self.coach.forward_message(message.channel, output)
