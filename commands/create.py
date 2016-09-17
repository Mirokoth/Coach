from config import config

pending = []

# Command: Create a tournament
# TODO: Implement a check to confirm creation
# TODO: Allow additional parameters and feedback
class Create():
    def __init__(self, message_handler, coach):
        self.command = "create"
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Create a new tournament with '{}{} <insert name>'.".format(config.BOT_CMD_SYMBOL, self.command)
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        # No arguments
        if arguments == False:
            await self.coach.forward_message(message.channel, "Gimme arguments brah.")
        # Arguments
        else:
            name = arguments[0]
            url = arguments[0]
            pending.append({'userId': message.author.id, 'type': 'create', 'action': [name, url]})
            await self.coach.forward_message(message.channel, "Are you sure you want to create a tournament called {}? Enter **y** or **n**.".format(name))
            for job in pending:
                print(job['userId'])
                print(job['type'])
                print(job['action'])

# Previous WIP below
# # Confirm command confirmation
# elif message.content.upper() == "Y":
#     for job in pending:
#         if job['userId'] == message.author.id:
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
#         if job['userId'] == message.author.id:
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
