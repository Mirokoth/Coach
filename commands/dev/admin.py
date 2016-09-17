# Dev Command: Determine if user is an administrator
class Admin():
    def __init__(self, message_handler, coach):
        self.command = "admin"
        self.message_handler = message_handler
        self.coach = coach

    async def on_message(self, message, command, arguments):
        isAdmin = self.coach.permissions.isAdmin(message.author)
        if isAdmin == True:
            res = "You have the power, " + message.author.name + "."
        else:
            res = "You have no power here."
        return await self.coach.forward_message(message.channel, res)
