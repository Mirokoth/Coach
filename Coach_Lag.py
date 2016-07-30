# modules
import asyncio

# third-party modules
import discord
import challonge

# config
import config

BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
client = discord.Client()
roles = []

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
# Log the number of tournaments found
print("{} tournaments found under this account.".format(len(challonge.tournaments.index())))

print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
print(tournament["started-at"]) # None

# --------------
# Helper Methods
# --------------

# Check if message is a command
def isCmd(message):
    if len(message) > 0 and message[0] == BOT_CMD_SYMBOL:
        return True
    return False

# Clean input
def sanitiseCmd(message):
    # Remove white space sequences
    message = ' '.join(message.split())
    # Grab words
    words = message.split(' ')
    return words

# Get command
def getCmd(message):
    words = sanitiseCmd(message)
    # Extract command
    command = words[0][1:].upper()
    return command

# Get arguments
def getArgs(message):
    words = sanitiseCmd(message)
    # Extract arguments
    arguments = words[1:]
    if len(arguments) == 0:
        return False
    return arguments

# --------------
# Discord Events
# --------------

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
        command = getCmd(message.content)
        arguments = getArgs(message.content)
        print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
        # Send message of to be logged
        # command_log(message.author.name, message.author.id, message.content)
    else:
        return

    # Command: Send brief details regarding a specific tournament
    if command == "META":
        # No argument provided
        if arguments == False:
            await client.send_message(message.channel, "Please add the ID of the tournament you wish to see. ie. If the URL is **http://challonge.com/test** then type **'{}{} test**'".format(BOT_CMD_SYMBOL, command.lower()))
        else:
            tournament = challonge.tournaments.show(arguments[0])
            await client.send_message(message.channel, "***Tournament details:***```ID: {}\nName: {}\nStarted at: {}\nState: {}```".format(tournament["id"],tournament["name"],tournament["started-at"],tournament["state"]))

    # Command: Send full responses for active tournaments associated to an account
    if command == "DETAILS":
        count = 0
        # Send details for each active tournament under this account
        for tournament in challonge.tournaments.index():
            count += 1
            output = "" # String to send
            # Start the message
            output += "\n**Tournament Details** for **{}**:\n ```".format(tournament["name"])
            # Append each property in the tournament
            for prop in tournament:
                output += "{}: {}\n".format(prop, tournament[prop])
            # Tie up the message
            output += "```"
            # Send all tournament details from Challonge response
            await client.send_message(message.channel, output)

    # Command: Die
    if command == "DIE":
        quit()

# Start Discord client
client.run(config.BOT_TOKEN)
