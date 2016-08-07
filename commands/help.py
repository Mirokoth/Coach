import asyncio
from config import config

class Help():
    def __init__(self, message_handler, coach):
        self.message_handler = message_handler
        self.coach = coach

    # Command description
    def get_description(self):
        description = "See this menu.. but how can we see this menu without first seeing this menu?"
        return description

    # Get all command descriptions
    def get_descriptions(self):
        plugins = self.message_handler.plugin_instances
        descriptions = {}
        for plugin in plugins:
            if "get_description" in dir(plugins[plugin]):
                desc = plugins[plugin].get_description()
                descriptions[plugin] = desc
                # Send command to module
            else:
                print("No description found for " + plugin + "!")
        return descriptions

    # Create help menu
    def generate_help(self):
        descriptions = self.get_descriptions()
        # Avoid printing empty menus
        if len(descriptions) == 0:
            return "Can't find the help menu! Contact your administrator."
        # Start the help menu
        help = 'Behold, the {} commandments!```'.format(len(descriptions))
        # Append each help item in alphabetical order
        # NOTE: A sorted dictionary returns a list, not a dictionary
        for key in sorted(descriptions):
            help += "{} - {}\n".format(key, descriptions[key])
        help += '```'
        return help

    # Process command
    async def on_message(self, message, command, arguments):
        res = self.generate_help()
        return await self.coach.forward_message(message.channel, res)
