import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

### Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_DISCOCATS_GROUP_ID = os.getenv("TELEGRAM_DISCOCATS_GROUP_ID", "")
TELEGRAM_DISCOCATS_CHANNEL_ID = int(os.getenv("TELEGRAM_DISCOCATS_CHANNEL_ID", "0"))
TELEGRAM_MUSIC_BOX_ID = int(os.getenv("TELEGRAM_MUSIC_BOX_ID", "0"))
BOT_ADMIN = int(os.getenv("BOT_ADMIN", "0"))


### Path
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
DOWNLOADS_DIR = BASE_DIR / "downloads"
SQLITE_DB_FILE = BASE_DIR / "quiz_bot.db"


### DataBase
# MONGO_USERNAME = os.getenv("MONGO_USERNAME", "")
# MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
