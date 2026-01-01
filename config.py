import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
MASTER_BOT_TOKEN = os.getenv("MASTER_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# comma separated IDs → 123,456,789
SUDO_USERS = list(
    map(int, os.getenv("SUDO_USERS", "").split(",")))