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


DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
client = discord.Client()
roles = []
server_lst = []

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
# Log the number of tournaments found


class proc_message():

	def __init__(self, message):
		self.message = message

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

	async def the_message(message):

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
				await self.coach.send_message(message.channel, teams_output)
			else:
				await self.coach.send_message('Could not work with argument {}'.format(arguments[0]))

		# Command: Die
		if command == "DIE":
			quit()

	#	self.command_list = json.load(open(commands.json))
	#	self.command_count = 0
	#	for seperate_command in command_list:
	#		if command == seperate_command:
	#			command_count =+ 1
	#			self.argument = seperate_command['command']
	#			await self.argument(message)
	#	if command_count == 0:
	#		await self.coach.send_message(message.channel, '{} is not a recognised command'.format(command))
