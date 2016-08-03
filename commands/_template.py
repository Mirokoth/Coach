### ------------------------------------------------
###  All of the below infomation should remain
###  You can add any modules or code required
###m  message.channel and the string to send can be changed.
### ------------------------------------------------

import asyncio
from coach import coach

class message():
    async def __new__(self, message, command, arguments):
        await coach.forward_message(message.channel, 'TEXT TO CHANGE'))
