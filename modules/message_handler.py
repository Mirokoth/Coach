# python
import asyncio
import json
import os
from importlib import import_module

# third-party
import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# bot modules
from modules.input import input

# config
from config import config

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL

# Challonge Credentials
challonge.set_credentials(config.CHAL_USER, config.CHAL_API)
# Retrieve a tournament by its id (or its url).
tournament = challonge.tournaments.show('Test_Tourno')
# Log the number of tournaments found
print("{} tournaments found under this account.".format(len(challonge.tournaments.index())))

# Dummy test
print(tournament["id"]) # 3272
print(tournament["name"]) # My Awesome Tournament
print(tournament["started-at"]) # None

class message_handler():

	# Set message to message
	def __init__(self, message):
		self.message = message

	async def the_message(message):
		CMDS = json.load(open(os.path.dirname(DIRECTORY) + '\\commands\\commands.json')) # Load list of commands and .py locations
		if input.isCmd(message.content):
			# Log command to console
			command = input.getCmd(message.content)
			arguments = input.getArgs(message.content)
			print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
		else:
			return

		found_command = False # Temp variable
		for separate_command in CMDS: # For each command in the command dictionary
			if command == str(separate_command).upper(): # If the command given matches a command in the dictionary
				found_command = True
				script = import_module(str(CMDS[separate_command])) # Import module referenced by command in dictionary
				await script.message(message, command, arguments) # Send message to module
			if found_command == True: # if a matching command was found, break the for loop
				break
		if found_command == False: # if no command was found return error
			script = import_module('commands.error')
			await script.message(message, command, arguments)
