from config import config

# Command: Create a tournament
# TODO: Implement a check to confirm creation
# TODO: Allow additional parameters and feedback
class Create():
    def __init__(self, message_handler, coach):
        self.command = "create"
        self.adminRequired = True
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Create a new tournament with '{}{} <insert name>'.".format(config.BOT_CMD_SYMBOL, self.command)
        return description

    async def on_message(self, message, command, arguments):
        userId = message.author.id

        # Continue creation process
        if self.message_handler.commandInProgress(self.command, userId) == True:
            # TODO: Add state switches
            print(self.message_handler.getCommandState(self.command, userId))
            print("Start command is in progress for " + userId)

            if arguments[0].upper() == "Y" or arguments[0].upper() == "YES":
                await self.coach.forward_message(message.channel, "Will add this to the backburner for you.")
            elif arguments[0].upper() == "N" or arguments[0].upper() == "NO":
                await self.coach.forward_message(message.channel, "Won't bother then.")
            else:
                await self.coach.forward_message(message.channel, "..Yes or no?")

            # TODO: Send request to API

        # Start new creation process
        else:
            # No arguments
            if arguments == False:
                await self.coach.forward_message(message.channel, self.get_description())

            # Arguments
            else:
                name = arguments[0]
                url = "beta-" + arguments[0]
                # Set the first command state for this user
                self.message_handler.setCommandState(self.command, userId, 1)
                # pending.append({'userId': userId, 'type': 'create', 'action': [name, url]})
                await self.coach.forward_message(message.channel, "Are you sure you want to create a tournament called {}? Enter **yes** or **no**.".format(name))
                # for job in pending:
                #     print(job['userId'])
                #     print(job['type'])
                #     print(job['action'])

# Previous WIP below
# # Confirm command confirmation
# elif message.content.upper() == "Y":
#     for job in pending:
#         if job['userId'] == userId:
#             # Create tournament
#             if job['type'] == 'create':
#                 print(job['action'])
#                 try:
#                     await challonge.tournaments.create(job['action'][0], job['action'][1])
#                     await client.forward_message(message.channel, "I think it worked")
#                     break
#                 except:
#                     await client.forward_message(message.channel, "'El problemo bromego.")
#     return
# # Decline command confirmation
# elif message.content.upper() == "N":
#     for job in pending:
#         if job['userId'] == userId:
#             await client.forward_message(message.channel, "Cancelling your fucking request.")
#             # Create tournament
#             # if job['type'] == 'create':
#             #     print(job['action'])
#             #     try:
#             #         await challonge.tournaments.create(job['action'][0], job['action'][1])
#             #         await client.forward_message(message.channel, "I think it worked")
#             #     except:
#             #         await client.forward_message(message.channel, "'El problemo bromego.")
#     return
