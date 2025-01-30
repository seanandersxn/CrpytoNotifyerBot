import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
from datetime import time

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))

def getFNG():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    data = response.json()
    return data["data"][0]["value"], data["data"][0]["value_classification"]

async def fngCommand(update: Update, context: CallbackContext) -> None:
    index, sentiment = getFNG()
    message = f"Fear & Greed Index: {index} ({sentiment})"
    await update.message.reply_text(message)

async def dailyFNG(context: CallbackContext) -> None:
    index, sentiment = getFNG()
    message = f"Daily Update: Fear and Greed Index: {index} ({sentiment})"
    await context.bot.send_message(chat_id=CHAT_ID, text=message)

async def getChatID(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    message = f"Chat ID: `{chat_id}`"
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("fgi", fngCommand))
    app.add_handler(CommandHandler("chatid", getChatID))

    job_queue = app.job_queue
    job_queue.run_daily(dailyFNG, time(hour=20, minute=55))

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()