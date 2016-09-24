import asyncio
from twilio.rest import TwilioRestClient

from config import config

# Command: Send SMS
class Sms():
    def __init__(self, message_handler, coach):
        self.command = "sms"
        self.adminRequired = True
        self.message_handler = message_handler
        self.coach = coach

    async def on_message(self, message, command, arguments):
        client = TwilioRestClient(config.TWIL_ACCOUNT_SID, config.TWIL_AUTH_TOKEN)
        txtContent = ''
        for text in arguments[1:len(arguments)]:
            txtContent += text + ' '
        txt = client.messages.create(
            body=txtContent,
            to=arguments[0],
            from_=config.TWIL_NUMBER,
        )

        res = 'SMS Sent:\nFrom: {}\nTo: {}\n\n{}'.format(config.TWIL_NUMBER, arguments[0], txtContent);
        return await self.coach.forward_message(message.channel, res)
