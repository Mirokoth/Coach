# modules
import asyncio
import json
import os
from importlib import import_module

# third-party modules
import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# config
import config

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
# Log the number of tournaments found


class proc_message():
	# Set message to message
	def __init__(self, message):
		self.message = message

	async def the_message(message, isCmd):
		CMDS = json.load(open(DIRECTORY + '\\commands.json')) # Load list of commands and .py locations
		if isCmd:
			# Log command to console
			command = check_cmd.getCmd(message.content)
			arguments = check_cmd.getArgs(message.content)
			print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
		else:
			return

		found_command = False # Temp variable
		for seperate_command in CMDS: # For each command in the command dictionary
			if command == str(seperate_command).upper(): # If the command given matches a command in the dictionary
				found_command = True
				script = import_module(str(CMDS[seperate_command])) # Import module referenced by command in dictionary
				await script.message(message, command, arguments) # Send message to module
			if found_command == True: # if a matching command was found, break the for loop
				break
		if found_command == False: # if no command was found return error
			script = import_module('commands.error')
			await script.message(message, command, arguments)


class check_cmd():

		# Clean input
		def sanitiseCmd(message):
			# Remove white space sequences
			message = ' '.join(message.split())
			# Grab words
			words = message.split(' ')
			return words

		# Get command
		def getCmd(message):
			words = check_cmd.sanitiseCmd(message)
			# Extract command
			command = words[0][1:].upper()
			return command

		# Get arguments
		def getArgs(message):
			words = check_cmd.sanitiseCmd(message)
			# Extract arguments
			arguments = words[1:]
			if len(arguments) == 0:
				return False
			return arguments
