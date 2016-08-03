from coach import coach
import os
from config import config

# --- CONFIG ---
BOT_TOKEN = config.BOT_TOKEN

# --- RUN BOT ---
coach.run(BOT_TOKEN)
