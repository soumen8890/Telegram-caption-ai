import os

import re

import datetime

import logging

from pyrogram import Client, filters

from pyrogram.enums import ParseMode

from pyrogram.types import Message

from dotenv import load_dotenv

from flask import Flask

# Configure logging

logging.basicConfig(

    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

    level=logging.INFO

)

logger = logging.getLogger(__name__)

# Load environment variables

load_dotenv()

# Bot configuration

API_ID = int(os.getenv("API_ID"))

API_HASH = os.getenv("API_HASH"))

BOT_TOKEN = os.getenv("BOT_TOKEN"))

TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")  # Channel username or ID

ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your user ID for admin commands

# Default HTML caption template

DEFAULT_CAPTION = """

<b>{filename}</b>

<code>Size:</code> <i>{filesize}</i>

<code>Type:</code> <i>{ext}</i>

"""

# Initialize Flask app

flask_app = Flask(__name__)

@flask_app.route('/')

def home():

    return '✅ Bot is running!'

def run_flask():

    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

# Initialize the bot

app = Client(

    "auto_caption_bot",

    api_id=API_ID,

    api_hash=API_HASH,

    bot_token=BOT_TOKEN,

    parse_mode=ParseMode.HTML

)

# Helper functions

def get_file_size(size):

    """Convert bytes to human-readable format"""

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:

        if size < 1024:

            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"

def extract_metadata(filename):

    """Extract metadata from filename"""

    metadata = {

        'filename': filename,

        'ext': os.path.splitext(filename)[1][1:].upper() if '.' in filename else 'Unknown',

        'year': None,

        'quality': None,

        'season': None,

        'episode': None,

        'language': None

    }

    

    # Common patterns in filenames

    patterns = {

        'year': r'(19|20)\d{2}',

        'quality': r'(720p|1080p|2160p|4K|HD|FHD|UHD|SD)',

        'season': r'S(\d{1,2})',

        'episode': r'E(\d{1,2})',

        'language': r'(English|Hindi|Bengali|Tamil|Telugu|Malayalam|Kannada)'

    }

    

    for key, pattern in patterns.items():

        match = re.search(pattern, filename, re.IGNORECASE)

        if match:

            metadata[key] = match.group(1) if key in ['season', 'episode'] else match.group()

    

    return metadata

def get_wish():

    """Get appropriate greeting based on time"""

    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:

        return "Good Morning"

    elif 12 <= hour < 17:

        return "Good Afternoon"

    elif 17 <= hour < 21:

        return "Good Evening"

    else:

        return "Good Night"

def format_caption(caption_template, metadata, file_size, additional_caption=""):

    """Format the caption using the template and metadata"""

    caption = caption_template.format(

        filename=metadata['filename'],

        filesize=get_file_size(file_size),

        caption=additional_caption,

        language=metadata['language'] or 'Unknown',

        year=metadata['year'] or 'Unknown',

        quality=metadata['quality'] or 'Unknown',

        season=metadata['season'] or 'Unknown',

        episode=metadata['episode'] or 'Unknown',

        ext=metadata['ext'],

        wish=get_wish()

    )

    return caption.strip()

# Bot commands

@app.on_message(filters.command("start") & filters.private)

async def start(client, message: Message):

    await message.reply_text(

        "🤖 <b>Auto Caption Bot</b>\n\n"

        "Forward any file to me and I'll add a caption and forward it to the channel.\n\n"

        "Use /setcaption to set a custom caption template.\n"

        "Use /getcaption to see the current template.",

        parse_mode=ParseMode.HTML

    )

@app.on_message(filters.command("setcaption") & filters.user(ADMIN_ID))

async def set_caption(client, message: Message):

    if len(message.command) < 2:

        await message.reply_text(

            "Please provide a caption template.\n\n"

            "Example:\n"

            "<code>/setcaption &lt;b&gt;{filename}&lt;/b&gt;\n"

            "&lt;code&gt;Size:&lt;/code&gt; &lt;i&gt;{filesize}&lt;/i&gt;\n"

            "&lt;code&gt;Type:&lt;/code&gt; &lt;i&gt;{ext}&lt;/i&gt;</code>",

            parse_mode=ParseMode.HTML

        )

        return

    

    global DEFAULT_CAPTION

    DEFAULT_CAPTION = message.text.split(" ", 1)[1]

    await message.reply_text("✅ <b>Caption template updated successfully!</b>", parse_mode=ParseMode.HTML)

@app.on_message(filters.command("getcaption") & filters.user(ADMIN_ID))

async def get_caption(client, message: Message):

    await message.reply_text(

        f"📝 <b>Current caption template:</b>\n\n<code>{DEFAULT_CAPTION}</code>\n\n"

        "<b>Available variables:</b>\n"

        "• <code>{filename}</code> - File name\n"

        "• <code>{filesize}</code> - File size\n"

        "• <code>{ext}</code> - File extension\n"

        "• <code>{language}</code> - Language from filename\n"

        "• <code>{year}</code> - Year from filename\n"

        "• <code>{quality}</code> - Quality from filename\n"

        "• <code>{season}</code> - Season from filename\n"

        "• <code>{episode}</code> - Episode from filename\n"

        "• <code>{wish}</code> - Time-based greeting",

        parse_mode=ParseMode.HTML

    )

# Main handler for files

@app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))

async def handle_files(client, message: Message):

    try:

        logger.info(f"Received file from user: {message.from_user.id}")

        

        # Get file information

        if message.document:

            file = message.document

            file_name = file.file_name

        elif message.video:

            file = message.video

            file_name = file.file_name or f"video.{file.mime_type.split('/')[-1]}"

        elif message.audio:

            file = message.audio

            file_name = file.file_name or f"audio.{file.mime_type.split('/')[-1]}"

        elif message.photo:

            file = message.photo

            file_name = f"photo.jpg"

        

        file_size = file.file_size

        metadata = extract_metadata(file_name)

        logger.info(f"Processing file: {file_name} ({get_file_size(file_size)})")

        

        # Get caption from message if available

        additional_caption = message.caption or ""

        

        # Format the caption

        caption = format_caption(DEFAULT_CAPTION, metadata, file_size, additional_caption)

        logger.info(f"Formatted caption: {caption}")

        

        # Send a processing message

        processing_msg = await message.reply_text("🔄 <b>Processing your file...</b>", parse_mode=ParseMode.HTML)

        

        # Forward the file to the channel with the new caption

        await message.copy(

            chat_id=TARGET_CHANNEL,

            caption=caption,

            parse_mode=ParseMode.HTML

        )

        

        # Update the processing message

        await processing_msg.edit_text("✅ <b>File forwarded to channel with caption!</b>", parse_mode=ParseMode.HTML)

        logger.info(f"File forwarded to channel: {TARGET_CHANNEL}")

    

    except Exception as e:

        error_msg = f"❌ <b>Error:</b> <code>{str(e)}</code>"

        await message.reply_text(error_msg, parse_mode=ParseMode.HTML)

        logger.error(f"Error processing file: {e}")

if __name__ == "__main__":

    # Start Flask server in a separate thread

    import threading

    flask_thread = threading.Thread(target=run_flask)

    flask_thread.start()

    

    # Start the bot

    logger.info("Starting bot...")

    app.run()

    logger.info("Bot stopped")
