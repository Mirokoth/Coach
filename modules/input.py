from config import config

class input():

    # Check if message is a command
    def isCmd(message):
        if len(message) > 0 and message[0] == config.BOT_CMD_SYMBOL:
            return True
        return False

    # Clean input
    def sanitiseCmd(message):
        # Remove white space sequences
        message = ' '.join(message.split())
        # Grab words
        words = message.split(' ')
        return words

    # Get command
    def getCmd(message):
        words = input.sanitiseCmd(message)
        # Extract command
        command = words[0][1:].upper()
        return command

    # Get arguments
    def getArgs(message):
        words = input.sanitiseCmd(message)
        # Extract arguments
        arguments = words[1:]
        if len(arguments) == 0:
            return False
        return arguments
