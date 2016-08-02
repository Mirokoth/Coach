from coach import coach

# --- CONFIG ---

DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # relative directory
GOOGLE_API = DIRECTORY + config.G_API
GSHEET_URL = config.GSHEET_URL
BOT_CMD_SYMBOL = config.BOT_CMD_SYMBOL
client = discord.Client()
roles = []
server_lst = []
client = coach()

# --- RUN BOT ---

client.run(config.BOT_TOKEN)
