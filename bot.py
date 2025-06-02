import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os

# Load environment variables from .env file for local development
load_dotenv()

# Configuration from config.py (or directly from os.environ)
# For simplicity, we'll use os.environ directly here, assuming it's set
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# API_ID and API_HASH are typically used with a Telegram client library (like Telethon or Pyrogram)
# which is different from a bot library. For this bot example, BOT_TOKEN is sufficient.

# You can define your caption formats here or load from config.py
DEFAULT_CAPTION_FORMAT = """
🎬 **{filename}** ({year})
✨ Quality: **{quality}**
📏 Resolution: **{resolution}** ({width}x{height})
💾 Size: **{filesize}**
⏳ Duration: **{duration}**
🗣️ Language: **{language}**
#️⃣ #{ext}
"""

AUDIO_CAPTION_FORMAT = """
🎶 **{title}** by **{artist}**
🎧 Type: **{ext}**
💾 Size: **{filesize}**
⏳ Duration: **{duration}**
"""

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    """Sends a message on /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! Send me a file and I'll try to caption it.",
    )

async def handle_document(update: Update, context):
    """Handles documents and attempts to caption them."""
    document = update.message.document
    
    # In a real bot, you'd extract metadata here.
    # For this example, we'll use placeholder data or derive from filename.
    
    file_name = document.file_name if document.file_name else "Unknown File"
    file_size = document.file_size
    mime_type = document.mime_type
    
    # Dummy parsing for variables - real parsing would be more robust
    # e.g., using regex for year, quality, etc.
    year = "N/A"
    quality = "N/A"
    language = "N/A"
    ext = file_name.split('.')[-1] if '.' in file_name else "N/A"
    
    if "video" in mime_type:
        # For video files, you'd typically get duration, width, height from video object
        # (This requires fetching file details or using a media parsing library like moviepy or ffprobe)
        # For this example, we'll use placeholders.
        duration = "N/A"
        width = "N/A"
        height = "N/A"
        resolution = "N/A" # or f"{width}x{height}" if available
        
        # Populate a dictionary with available variables
        caption_data = {
            "filename": file_name,
            "filesize": f"{file_size / (1024*1024):.2f} MB" if file_size else "N/A",
            "year": year,
            "quality": quality,
            "duration": duration,
            "width": width,
            "height": height,
            "resolution": resolution,
            "language": language,
            "ext": ext,
            "mime_type": mime_type,
            "caption": "", # Original caption, if any
            "season": "N/A", "episode": "N/A", # For TV shows, requires filename parsing
            "title": "N/A", "artist": "N/A", # For audio, requires ID3 tag reading
            "wish": "N/A" # Dynamic wish like Good Morning
        }
        
        try:
            caption_text = DEFAULT_CAPTION_FORMAT.format(**caption_data)
        except KeyError as e:
            caption_text = f"Error formatting caption: Missing variable {e}. Raw Data: {caption_data}"
            logger.error(caption_text)

    elif "audio" in mime_type:
        # For audio, you'd extract title/artist from metadata if possible
        title = file_name.split('.')[0] if '.' in file_name else "Unknown Title"
        artist = "Unknown Artist"
        duration = "N/A" # Get from audio metadata
        
        caption_data = {
            "filename": file_name,
            "filesize": f"{file_size / (1024*1024):.2f} MB" if file_size else "N/A",
            "duration": duration,
            "ext": ext,
            "mime_type": mime_type,
            "title": title,
            "artist": artist,
            "caption": "", # Original caption, if any
            # Other variables will be N/A for audio files
        }
        try:
            caption_text = AUDIO_CAPTION_FORMAT.format(**caption_data)
        except KeyError as e:
            caption_text = f"Error formatting caption: Missing variable {e}. Raw Data: {caption_data}"
            logger.error(caption_text)
    else:
        # Fallback for other file types
        caption_data = {
            "filename": file_name,
            "filesize": f"{file_size / (1024*1024):.2f} MB" if file_size else "N/A",
            "ext": ext,
            "mime_type": mime_type,
            "caption": "", # Original caption, if any
            # All other variables will be N/A
            "year": "N/A", "quality": "N/A", "duration": "N/A", "width": "N/A",
            "height": "N/A", "resolution": "N/A", "language": "N/A",
            "season": "N/A", "episode": "N/A", "title": "N/A", "artist": "N/A",
            "wish": "N/A"
        }
        caption_text = f"📁 **{file_name}**\n📦 Size: {caption_data['filesize']}\n📄 Type: {mime_type}"

    await update.message.reply_text(caption_text, parse_mode='Markdown')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


