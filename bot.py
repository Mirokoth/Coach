# modules
import asyncio
import json
import os

# third-party modules
import discord
import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# config
import config
from config import config

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
DIR_CONF_TOURNY = DIRECTORY + '/config/tournaments.json'

# New installation
if os.path.exists(DIR_CONF_TOURNY) == False:
    # Enter setup mode
    setupMode = True

# Existing installation
else:
    setupMode = False
    # Grab tournament configuration
    tournaments = json.load(open(DIR_CONF_TOURNY))

# Fill tournament details with dummy data
# NOTE: To replace this with a setup mode for configuration via Discord
if setupMode == True:
    tournaments = ['Test_Tourno'] # Assign dev dummy data
    # data = 'arbitrary'
    # with open(DIR_CONF_TOURNY, 'w') as outfile:
    #     json.dump(data, outfile)

GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
client = discord.Client()
roles = []
server_lst = []

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show(tournaments[0])
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
    # Cache server list
    for server in client.servers:
        server_lst.append(server)
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


    if command == "MATCHES": # Gets match details for provided Tournament

        if arguments == False:
            await client.send_message(message.channel, "No Tournament details or command switches provided")
        elif len(arguments) > 1:
            if arguments[1].upper() == "WINNER": # If second argument given is winner provide only match win details
                argument_count = 0 # Count how many matches have been won so far
                for match in challonge.matches.index(arguments[0]):
                    if "NONE" not in str(match['winner-id']).upper():
                        argument_count =+ 1
                        participant = challonge.participants.show(arguments[0], match['winner-id'])
                        #await client.send_message(message.channel, 'Round {} winner: {}'.format(match['round'],participant['name']))
                        await client.send_message(server_lst[0], 'Round {} winner: {}'.format(match['round'],participant['name'])) # Outputs to servers default channel
                # If no matches won yet, return information
                if argument_count <= 0:
                    await client.send_message(server_lst[0], 'No matches have been won yet.')
        elif len(arguments) == 1:
            for match in challonge.matches.index(arguments[0]):
                output = ""  # String to send
                for details in match:
                    output += "{}: {}\n".format(details,match[details])
                await client.send_message(message.channel, "```{}```".format(output))


    # Command: Running tests on google spreadsheet integration for team and user database
    # currently running tests off sheet - https://docs.google.com/spreadsheets/d/14f_bEIFMrpuE2euix-r1IC2zA-_u0tQKGnRarbihZvA/edit?usp=sharing
    if command == "TSTSHEET":
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API, scope)
        gc = gspread.authorize(credentials)
        print(GSHEET_URL)
        sheet = gc.open_by_url(GSHEET_URL)
        worksheet = sheet.get_worksheet(0)
        if arguments[0] == "TEAMS":
            teams_output = ''
            teams = worksheet.col_values(1)
            for name in teams:
                if len(name) > 1:
                    if name in teams_output or name == worksheet.acell('A1').value:
                        print(name)
                        pass
                    else:
                        teams_output += "{}\n".format(name)
            await client.send_message(message.channel, teams_output)
        else:
            await client.send_message('Could not work with argument {}'.format(arguments[0]))

    # Command: Die
    if command == "DIE":
        quit()

# Start Discord client
client.run(config.BOT_TOKEN)
