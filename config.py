import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    MONGO_URI = os.getenv("MONGO_URI")
    
    @classmethod
    def validate(cls):
        required = [cls.BOT_TOKEN, cls.MONGO_URI]
        if not all(required):
            raise ValueError("Missing required environment variables")
