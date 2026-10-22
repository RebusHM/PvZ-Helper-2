import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Telegram Bot Credentials
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@NewsForPvZ")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/NewsForPvZ")
BOT_USERNAME = os.getenv("BOT_USERNAME", "HelperPvZ2bot")

# Optional Proxy and Custom API Base URL for bypassing network blocks
PROXY_URL = os.getenv("PROXY_URL", "")
API_BASE_URL = os.getenv("API_BASE_URL", "")

# Local Telegram Bot API Server (tdlib/telegram-bot-api)
# Unlocks 2000MB (2GB) file upload limit instead of cloud Telegram 50MB limit!
# Obtain API_ID and API_HASH from https://my.telegram.org
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
USE_LOCAL_BOT_API = os.getenv("USE_LOCAL_BOT_API", "false").lower() in ("true", "1", "yes")
LOCAL_BOT_API_PORT = int(os.getenv("LOCAL_BOT_API_PORT", "8081"))

# Admin IDs (comma-separated integer IDs)
_admins_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i.strip()) for i in _admins_raw.split(",") if i.strip().isdigit()]

# Allowed Chat IDs for Multiverse PvZ network (optional numeric IDs)
_allowed_chats_raw = os.getenv("ALLOWED_CHAT_IDS", "")
ALLOWED_CHAT_IDS = [
    int(i.strip()) for i in _allowed_chats_raw.split(",")
    if i.strip().lstrip("-").isdigit()
]

# Google Play Tracker Configuration
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "10"))

# Package identifiers on Google Play
PVZ2_PACKAGE_ROW = "com.ea.game.pvz2_row"
PVZ2_PACKAGE_NA = "com.ea.game.pvz2_na"
PVZ3_PACKAGE = "com.ea.gp.pvzn3xt"

# Paths
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VERSIONS_FILE = DATA_DIR / "versions.json"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Telegram Custom Premium Emoji IDs (from NewsEmoji and PvZ sets)
EMOJI_GOOGLE_PLAY_ID = "5931594395508805861"
EMOJI_DOWNLOAD_ID = "5435977112538324435"
EMOJI_PVZ2_ID = "5249112379798628360"
EMOJI_PVZ3_ID = "5444974179965250455"
EMOJI_CHECK_PVZ2_ID = "5217782972786189258"
EMOJI_CHECK_PVZ3_ID = "5426948575886087620"
EMOJI_WARNING_ID = "5447644880824181073"
EMOJI_CHANNEL_ID = "5424818078833715060"
EMOJI_CHAT_ID = "5467538555158943525"

# Additional Premium Emojis from NewsEmoji pack
EMOJI_SEARCH_ID = "5231012545799666522"     # 🔍
EMOJI_REFRESH_ID = "5375338737028841420"    # 🔄
EMOJI_LIGHTNING_ID = "5456140674028019486"  # ⚡
EMOJI_STATS_ID = "5231200819986047254"      # 📊
EMOJI_STAR_ID = "5438496463044752972"       # ⭐
EMOJI_CHECK_ID = "5206607081334906820"      # ✔️
EMOJI_CROSS_ID = "5210952531676504517"      # ❌
EMOJI_INFO_ID = "5334544901428229844"       # ℹ️
EMOJI_SETTINGS_ID = "5341715473882955310"   # ⚙️
EMOJI_CALENDAR_ID = "5413879192267805083"   # 🗓
EMOJI_FIRE_ID = "5424972470023104089"       # 🔥
EMOJI_HOURGLASS_ID = "5386367538735104399"  # ⌛
EMOJI_IDEA_ID = "5422439311196834318"       # 💡
EMOJI_ROCKET_ID = "5224607267797606837"     # 🚀
EMOJI_PACKAGE_ID = "5406683434124859552"    # 🛍 / 📦
EMOJI_ARROW_ID = "5416117059207572332"      # ➡️ / 🔹
EMOJI_PIN_ID = "5397782960512444700"        # 📌
EMOJI_INBOX_ID = "6096080291347042802"      # 📥
EMOJI_SPARKLES_ID = "5325547803936572038"   # ✨
EMOJI_BOT_ID = "5341715473882955310"        # 🤖 / ⚙️
EMOJI_TAG_ID = "5222444124698853913"        # 🏷 / 🔖
EMOJI_DIAMOND_ID = "5427168083074628963"    # 💎
EMOJI_DOWN_ARROW_ID = "5406745015365943482" # ⬇️
EMOJI_GAMEPAD_ID = "5361741454685256344"    # 🎮
EMOJI_DISCORD_ID = "5325612636467903082"    # 📱 / Discord logo

