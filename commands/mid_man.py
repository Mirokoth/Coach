import asyncio
import os
import json
import coach

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
serverListJson = DIRECTORY + '\\server_list.json'

class mid_man():
    async def __new__(string, server_list):
        print(string)
        await coach.Coach.mid_man(server_list[0], string)
