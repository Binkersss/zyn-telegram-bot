import os
import datetime
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.zyn_tracker
collection = db.usage

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def track_zyn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    today = datetime.date.today().isoformat()
    
    # Find or create user entry
    collection.update_one(
        {"user_id": user_id, "date": today},
        {"$inc": {"count": 1}},
        upsert=True
    )

    count = collection.find_one({"user_id": user_id, "date": today})["count"]
    await update.message.reply_text(f"Zyn count for today: {count}")

async def daily_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    today = datetime.date.today().isoformat()
    
    entry = collection.find_one({"user_id": user_id, "date": today})
    count = entry["count"] if entry else 0

    await update.message.reply_text(f"Today's Zyn count: {count}")

async def weekly_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=6)
    
    total = 0
    summary = []
    
    for i in range(7):
        day = (week_ago + datetime.timedelta(days=i)).isoformat()
        entry = collection.find_one({"user_id": user_id, "date": day})
        count = entry["count"] if entry else 0
        summary.append(f"{day}: {count}")
        total += count
    
    await update.message.reply_text(f"Last 7 days Zyn count:\n" + "\n".join(summary) + f"\nTotal: {total}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("zyn", track_zyn))
    application.add_handler(CommandHandler("daily", daily_summary))
    application.add_handler(CommandHandler("weekly", weekly_summary))

    application.run_polling()

if __name__ == "__main__":
    main()
# This bot tracks Zyn usage and provides daily and weekly summaries.