### ------------------------------------------------
###  All of the below infomation should remain
###  You can add any modules or code required
###m  message.channel and the string to send can be changed.
### ------------------------------------------------

import asyncio
from coach import coach

pending = []

# Command: Create a tournament
# TODO: Implement a check to confirm creation
# TODO: Allow additional parameters and feedback
class message():
    async def __new__(self, message, command, arguments):
        # No arguments
        if arguments == False:
            await coach.forward_message(message.channel, "Gimme arguments brah.")
        # Arguments
        else:
            name = arguments[0]
            url = arguments[0]
            pending.append({'userId': message.author.id, 'type': 'create', 'action': [name, url]})
            await coach.forward_message(message.channel, "Are you sure you want to create a tournament called {}? Enter **y** or **n**.".format(name))
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
#                     await client.send_message(message.channel, "I think it worked")
#                     break
#                 except:
#                     await client.send_message(message.channel, "'El problemo bromego.")
#     return
# # Decline command confirmation
# elif message.content.upper() == "N":
#     for job in pending:
#         if job['userId'] == message.author.id:
#             await client.send_message(message.channel, "Cancelling your fucking request.")
#             # Create tournament
#             # if job['type'] == 'create':
#             #     print(job['action'])
#             #     try:
#             #         await challonge.tournaments.create(job['action'][0], job['action'][1])
#             #         await client.send_message(message.channel, "I think it worked")
#             #     except:
#             #         await client.send_message(message.channel, "'El problemo bromego.")
#     return
