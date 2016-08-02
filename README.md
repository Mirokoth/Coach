# Coach
Extdernal message handling via json file is currently working (on my pc at least).

bot.py - launches app
coach.py - intercepts and sends messages.
proc_message - "process_message" Message is send here for cleaning and then checking against commands.json
commands.json - command name followed by command python file e.g. "help": "commands.help"

commands folder:
currently holds two test commands.
These can be used as templates for future commands.
They use asyncio to send the message back to coach.py.
Requires def __new__ instead of __init__ because... well apparently you cant assign __init__ values.


------------------------------------------------

This needs a lot of cleaning but it is late.
