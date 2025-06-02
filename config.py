import os

# Get your Bot Token from BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Get your API ID and API Hash from my.telegram.org
API_ID = int(os.environ.get("API_ID", "YOUR_API_ID_HERE")) # Ensure it's an integer
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH_HERE")

# Your Telegram User ID (for admin commands, if any)
ADMINS = [int(admin_id) for admin_id in os.environ.get("ADMINS", "YOUR_ADMIN_ID_HERE").split(',')]

# Default caption format using your variables
DEFAULT_CAPTION_FORMAT = """
🎬 **{filename}** ({year})
✨ Quality: **{quality}**
📏 Resolution: **{resolution}** ({width}x{height})
💾 Size: **{filesize}**
⏳ Duration: **{duration}**
🗣️ Language: **{language}**
#️⃣ #{ext}
"""

# You can add more formats here based on mime_type or other criteria
AUDIO_CAPTION_FORMAT = """
🎶 **{title}** by **{artist}**
🎧 Type: **{ext}**
💾 Size: **{filesize}**
⏳ Duration: **{duration}**
"""

