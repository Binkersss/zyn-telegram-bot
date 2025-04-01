import os
import datetime
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from flask import Flask

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.zyn_tracker_test
collection = db.usage

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Zyn Tracker Bot is running!"

async def delete_old_entries():
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    collection.delete_many({"date": {"$lt": thirty_days_ago.isoformat()}})
    logger.info("Deleted entries older than 30 days.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/zyn - Track Zyn usage\n"
        "/daily - Daily summary\n"
        "/weekly - Weekly summary\n"
        "/30days - 30-day summary\n"
        "/removeRecent - Remove the most recent entry\n"
        "/deleteAll - Delete all entries\n"
        "/help - Show this help message"
    )

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

async def thirty_day_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=29)

    total = 0
    
    for i in range(30):
        day = (thirty_days_ago + datetime.timedelta(days=i)).isoformat()
        entry = collection.find_one({"user_id": user_id, "date": day})
        count = entry["count"] if entry else 0
        total += count
    await update.message.reply_text(f"Last 30 days Zyn count: {total}")

async def delete_all_entries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    collection.delete_many({"user_id": user_id})
    await update.message.reply_text("All entries deleted.")

async def decrement_most_recent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    today = datetime.date.today().isoformat()
    
    # Decrement the count by 1
    result = collection.update_one(
        {"user_id": user_id, "date": today},
        {"$inc": {"count": -1}}
    )
    
    if result.modified_count > 0:
        await update.message.reply_text("Removed most recent entry.")
    else:
        await update.message.reply_text("No entry found to remove.")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("zyn", track_zyn))
    application.add_handler(CommandHandler("daily", daily_summary))
    application.add_handler(CommandHandler("weekly", weekly_summary))
    application.add_handler(CommandHandler("30days", thirty_day_summary))
    application.add_handler(CommandHandler("removeRecent", decrement_most_recent))
    application.add_handler(CommandHandler("deleteAll", delete_all_entries))
    application.add_handler(CommandHandler("help", help))

    application.job_queue.run_daily(delete_old_entries, time=datetime.time(hour=0, minute=0, second=0))

    application.run_polling()

if __name__ == "__main__":
    # Run the Flask app in a separate thread
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.start()
    
    # Run the main bot application
    main()
