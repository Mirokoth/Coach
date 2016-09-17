# config-defaults
# note: rename this file to 'config.py' to override

# Credentials/tokens
BOT_TOKEN = "<insert>" # Discord API token
CHAL_USER = "<insert>" # Challonge username
CHAL_API = "<insert>" # Challonge API token
G_API = "<insert>" # Google's authentication credentials file name
GSHEET_URL = "<insert>" # URL for the Google Docs spreedsheet

# Server settings
PYTHON_CMD = "python" # Python environment variable (usually python/python3)
COMMAND_LOG = "log.txt" # Log file name

# Application settings
BOT_CMD_SYMBOL = "!" # Symbol prefix used to trigger bot commands

ADMIN_ROLE_IDS = [
    "<roleID>",
    "<roleID>"
]

ENABLED_COMMANDS = {
    "Admin": True,
    "Create": True,
    "Details": True,
    "Gsheet": True,
    "Help": True,
    "Meta": True,
    "Quit": True
}
