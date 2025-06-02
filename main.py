import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from pymongo import MongoClient

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AutoCaptionBot:
    def __init__(self):
        self.config = Config()
        self.db = MongoClient(self.config.MONGO_URI)['AutoCaptionDB']
        self.templates = self.db['templates']
        
        self.app = Application.builder().token(self.config.BOT_TOKEN).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("set_template", self.set_template))
        self.app.add_handler(MessageHandler(
            filters.DOCUMENT | filters.VIDEO | filters.AUDIO | filters.PHOTO,
            self.handle_media
        ))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != self.config.OWNER_ID:
            return await update.message.reply_text("⚠️ Unauthorized!")
            
        await update.message.reply_html(
            "⚡ <b>Auto Caption Bot</b> ⚡\n\n"
            "📌 <code>/set_template</code> - Set your caption template\n\n"
            "Available variables:\n"
            "• filename, filesize, caption\n"
            "• language, year, quality\n"
            "• season, episode, duration\n"
            "• height, width, ext\n"
            "• resolution, mime_type\n"
            "• title, artist, wish"
        )
    
    async def set_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != self.config.OWNER_ID:
            return
            
        template = ' '.join(context.args)
        if not template:
            return await update.message.reply_text("Please provide a template")
            
        self.templates.update_one(
            {"_id": "default"},
            {"$set": {"template": template}},
            upsert=True
        )
        await update.message.reply_text("✅ Template updated!")
    
    async def handle_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            message = update.effective_message
            file = (message.document or message.video or 
                   message.audio or message.photo[-1] if message.photo else None)
            if not file:
                return
                
            # Get saved template
            saved = self.templates.find_one({"_id": "default"})
            template = saved.get("template", self._default_template()) if saved else self._default_template()
            
            # Prepare variables
            caption_vars = {
                "filename": file.file_name or "",
                "filesize": self._format_size(file.file_size),
                "caption": message.caption or "",
                "ext": file.file_name.split('.')[-1] if file.file_name else "",
                "mime_type": file.mime_type,
                "wish": self._get_greeting()
            }
            
            # Apply template
            new_caption = template.format(**caption_vars)
            await message.edit_caption(caption=new_caption)
            
        except Exception as e:
            logger.error(f"Error: {e}")

    def _default_template(self):
        return """<b>{filename}</b>
<code>📁 {filesize} | 🎞️ {ext}</code>
{wish}"""
    
    def _format_size(self, size):
        units = ['B', 'KB', 'MB', 'GB']
        for unit in units:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} GB"
    
    def _get_greeting(self):
        from datetime import datetime
        hour = datetime.now().hour
        if hour < 12: return "🌞 Good Morning"
        if hour < 17: return "☀️ Good Afternoon"
        return "🌙 Good Evening"
    
    def run(self):
        self.app.run_polling()

if __name__ == "__main__":
    bot = AutoCaptionBot()
    bot.run()
