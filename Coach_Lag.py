# modules
import asyncio

# third-party modules
import discord
import challonge

# config
import config

# Permanent Defenitons
BOT_CMD_SYMBOL = '!'
client = discord.Client()
roles = []

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
print(tournament["started-at"]) # None

'''
Helper Methods
'''

# Check if message is a command
def isCmd(message):
    if len(message) > 0 and message[0] == BOT_CMD_SYMBOL:
        return True
    return False


# Bot Ready
@client.event
async def on_ready():
    print('Logged in as {} ({}) with the following connected servers..'.format(client.user.name, client.user.id))
    print('------')
    for server in client.servers:
        print('{} ({})'.format(server.name, server.id))
        print('------')
    # Cache server roles
    print('Roles')
    print('------')
    for role in server.roles:
        roles.append(role)
        print(role.name + ' (' + role.id + ')')
    print('------')
    print('Get this guy a jockstrap and a cookie!')
    print('------')

# Message Received
@client.event
async def on_message(message):

    # Check if message is a command
    if isCmd(message.content):
        # Log command to console
        command = message.content.split(' ')[0][1:].upper()
        print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
        # Send message of to be Logged
        #command_log(message.author.name, message.author.id, message.content)

    else:
        return

    # Extract arguments
    arguments = message.content.split(' ')[1:]
    if len(arguments) == 0:
        arguments = False
    # await client.send_message(message.channel, "command: {}".format(command))
    # await client.send_message(message.channel, "arguments: {}".format(arguments))

    if command == "DETAILS":
        await client.send_message(message.channel, "***Tournoment details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))
    if command =="EXT_DET":
        output = ''
        for x in tournament:
            output += '{}: {}\n'.format(x,tournament[x])
        await client.send_message(message.channel, "***Full Tournoment Details:\n ```{}``` ".format(output))
    if command == "DIE":
        quit()

# Start Discord client
client.run(config.BOT_TOKEN)
