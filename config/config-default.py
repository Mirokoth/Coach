# config-defaults
# note: rename this file to 'config.py' to override

# Credentials/tokens
BOT_TOKEN = "<insert>" # Discord API token
CHAL_USER = "<insert>" # Challonge username
CHAL_API = "<insert>" # Challonge API token

# Optional credentials/tokens
G_API = "<insert>" # Google's authentication credentials file name
GSHEET_URL = "<insert>" # URL for the Google Docs spreedsheet
TWIL_ACCOUNT_SID = "XXXXXXXXXXXXXXXXX" # Twilio API ID
TWIL_AUTH_TOKEN = "XXXXXXXXXXXXXXXXX" # Twilio API token
TWIL_NUMBER = "XXXXXXXXX" # Twilio phone number

# Server settings
PYTHON_CMD = "python" # Python environment variable (usually python/python3)
COMMAND_LOG = "log.txt" # Log file name

# Application settings
BOT_CMD_SYMBOL = "!" # Symbol prefix used to trigger bot commands
CHAL_POLL_ENABLED = False # Enable Challonge polling for events (ie. Tournament completed)
CHAL_POLL_FREQUENCY = 30 # Frequency in seconds to poll Challonge tournaments for changes (default: 30, number in seconds)
FORFEIT_TIMEOUT = 30 # Number of minutes a team has until they forfeit a match. The counter begins once the match is announced.
QUOTE_ON_QUIT = True # Will Coach send a random quote to the channel when and administrator calls the "quit" command

ADMIN_ROLE_IDS = [ # Whitelist of role IDs for administrators
    "<roleID>",
    "<roleID>"
]

ENABLED_COMMANDS = { # Enable/disable commands
    "Admin": True,
    "Create": True,
    "Details": True,
    "Gsheet": True,
    "Help": True,
    "Meta": True,
    "Quit": True,
    "Sms": False,
    "Start": True
}
