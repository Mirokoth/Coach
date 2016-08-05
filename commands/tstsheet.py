### ------------------------------------------------
###  All of the below infomation should remain
###  You can add any modules or code required
###m  message.channel and the string to send can be changed.
### ------------------------------------------------

import asyncio
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import config

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL

class Tstsheet():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command received
    async def on_message(self, message, command, arguments):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API, scope)
        gc = gspread.authorize(credentials)
        print(GSHEET_URL)
        sheet = gc.open_by_url(GSHEET_URL)
        worksheet = sheet.get_worksheet(0)
        if arguments == False:
            await self.coach.forward_message(message.channel, "No command switches provided")
        if len(arguments) == 1:
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
