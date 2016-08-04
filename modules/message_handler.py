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

# test
from commands.help import Help

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
	list = json.load(open(os.path.dirname(DIRECTORY) + '\\commands\\commands.json'))
	commands = []
	for command in list:
		commands.append(command)
		# print(command)
	return commands

class message_handler():

	# Set message to message
	def __init__(self, coach):
		self.coach = coach

	async def the_message(self, message):
		print('the message')
		print(message)
		CMDS = json.load(open(os.path.dirname(DIRECTORY) + '\\commands\\commands.json')) # Load list of commands and .py locations
		if input.isCmd(message.content):
			# Log command to console
			command = input.getCmd(message.content)
			arguments = input.getArgs(message.content)
			print("{} ({}) used the following command: {}".format(message.author.name, message.author.id, command))
		else:
			return

		# TODO: Loop over modules and instantiate

		# Temporary catch
		if command.upper() == "GET":
			print('Gotten..')
			commands = get_commands()
			for command in commands:
				print(command)
			# print(self.message)
			# print(self.coach)
			# await self.coach.forward_message(message.channel, "Commands: {}".format(commands))
			return

		# Temporary catch
		if command.upper() == "HELP":
			print("Func: new help")
			plugin_instance = Help(self.coach) # help module
			await plugin_instance.test(message, command, arguments)

		# Previous catch loop
		# found_command = False # Temp variable
		# for separate_command in CMDS:
		# 	if command == str(separate_command).upper(): # If the command given matches a command in the dictionary
		# 		found_command = True
		# 		script = import_module(str(CMDS[separate_command])) # Import module referenced by command in dictionary
		# 		await script.message(message, command, arguments) # Send message to module
		# 	if found_command == True: # if a matching command was found, break the for loop
		# 		break
		# if found_command == False: # if no command was found return error
		# 	script = import_module('commands.error')
		# 	await script.message(message, command, arguments)

	async def get_commands(message):
		await get_commands()

		# import_module(str(list[command]))
        # storage = await self.get_storage(server)
        # commands = sorted(await storage.smembers('commands'))
        # cmds = []
        # for command in commands:
        #     cmd = {
        #         'name': command
        #     }
        #     cmds.append(cmd)
        # return cmds

	# async def get_commands():
	# 	CMDS = json.load(open(os.path.dirname(DIRECTORY) + '\\commands\\commands.json'))
	# 	# For each command in the command dictionary
	# 	for separate_command in CMDS:
	# 		script = import_module(str(CMDS[separate_command]))
	# 		await script.get_description() # Send message to module
