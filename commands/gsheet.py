import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import config

DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL

# Command: Read team information from a spreadsheet
class Gsheet():
    def __init__(self, message_handler, coach):
        self.command = "gsheet"
        self.message_handler = message_handler
        self.coach = coach

    def get_description(self):
        description = "Play with data in a google sheet using '{}{} teams'".format(config.BOT_CMD_SYMBOL, self.command)
        return description

    # Process command
    async def on_message(self, message, command, arguments):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API, scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_url(GSHEET_URL)
        worksheet = sheet.get_worksheet(0)
        if arguments == False:
            await self.coach.forward_message(message.channel, "No command switches provided.")
        elif len(arguments) == 1:
            if arguments[0].upper() == "TEAMS":
                teams_output = ''
                teams = worksheet.col_values(1)
                for name in teams:
                    if len(name) > 1:
                        if name in teams_output or name == worksheet.acell('A1').value:
                            print(name)
                            pass
                        else:
                            teams_output += "{}\n".format(name)
                await self.coach.forward_message(message.channel, teams_output)
            else:
                await self.coach.forward_message(message.channel, 'Could not work with argument **{}**'.format(arguments[0]))
