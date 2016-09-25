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

def get_commands():
	# Get all commands from the commands definition
	allCommands = json.load(open(os.path.dirname(DIRECTORY) + '\\commands\\definition.json'))
	# Enable commands based on user config
	commands = {}
	for command in allCommands:
		# Enabled
		if config.ENABLED_COMMANDS[command] == True:
			commands[command] = allCommands[command]
	return commands

class message_handler():

	# Set message to message
	def __init__(self, coach):
		self.coach = coach
		self.commandStates = {}

		# Get command list
		commands = get_commands()
		self.plugin_instances = {} # Empty dictionary for caching plugins

		# Dynamically load modules based on command list
		for command in commands:
			plugin = import_module(commands[command]) # load module
			plugin = getattr(plugin, command) # load class
			self.plugin_instances[command] = plugin(self, self.coach) # instantiate the class

	# Message received
	async def on_message(self, message):
		""" Read messages from Discord and process any commands found

		Args:
			message (obj):	Discord message object

		"""

		# Command found
		if input.isCmd(message.content):
			# Log command to console
			command = input.getCmd(message.content)
			arguments = input.getArgs(message.content)
			print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))

		# Command not found
		else:
			return

		match = False
		# Match against command list
		for plugin in self.plugin_instances:

			# Valid command
			if command.title() == plugin:

				# Admin required and user is admin
				if self.plugin_instances[command.title()].adminRequired == True and self.coach.permissions.isAdmin(message.author):
				    # Send command to module
					match = True
					await self.plugin_instances[command.title()].on_message(message, command, arguments)

				# Admin not required
				elif self.plugin_instances[command.title()].adminRequired == False:
					# Send command to module
					match = True
					await self.plugin_instances[command.title()].on_message(message, command, arguments)

				# Command not allowed
				else:
					pass

		# Invalid command
		if match == False:
			print("That ain't a command! Type {}help for more information.".format(BOT_CMD_SYMBOL))

	def getCommandState(self, command, userId):
		"""Get command state for a user

		Args:
			command (string): 	Command name
			userId (string):	Unique user ID

		Returns:
			bool: True if this command is in progress for this user, False if not.

		"""
		return self.commandStates.get(command)

	def commandInProgress(self, command, userId):
		"""Confirm whether a command is in progress for a user

		Args:
			command (string): 	Command name
			userId (string):	Unique user ID

		Returns:
			bool: True if this command is in progress for this user, False if not.

		"""
		if self.commandStates.get(command) == None:
				return False
		elif self.commandStates[command].get(userId) == None:
				return False
		return True

	def setCommandState(self, command, userId, state):
		"""Set command state for a user
		"""
		if self.commandStates.get(command) == None:
			self.commandStates[command] = {}
		self.commandStates[command][userId] = state
