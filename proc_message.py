# modules
import asyncio
import json
import os
import coach
from importlib import import_module

# third-party modules
#import discord
import challonge
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# config
import config


DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
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

	async def the_message(message, isCmd):
		CMDS = json.load(open(DIRECTORY + '\\commands.json'))
		if isCmd:
			# Log command to console
			command = check_cmd.getCmd(message.content)
			arguments = check_cmd.getArgs(message.content)
			print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
			# Send message of to be logged
			# command_log(message.author.name, message.author.id, message.content)
		else:
			return

		# Command: Die
		if command == "DIE":
			quit()

		command_count = 0
		for seperate_command in CMDS:
			print(str(seperate_command).upper())
			if command == str(seperate_command).upper():
				command_count =+ 1
				print(CMDS[seperate_command])
				script = str(CMDS[seperate_command])
				script = import_module(script)
				await script.message(message, command, arguments)
		if command_count == 0:
			print('Unable to find command - {}'.format(command))
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


	#	self.command_list = json.load(open(commands.json))
	#	self.command_count = 0
	#	for seperate_command in command_list:
	#		if command == seperate_command:
	#			command_count =+ 1
	#			self.argument = seperate_command['command']
	#			await self.argument(message)
	#	if command_count == 0:
	#		await self.coach.send_message(message.channel, '{} is not a recognised command'.format(command))
