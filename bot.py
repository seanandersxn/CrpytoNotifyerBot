import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def getFNG():
    url = "https://api.alternative.me/fng/"
    response = requests.get(url)
    data = response.json()
    return data["data"][0]["value"], data["data"][0]["value_classification"]

async def fngCommand(update: Update, context: CallbackContext) -> None:
    index, sentiment = getFNG()
    message = f"Fear & Greed Index: {index} ({sentiment})"
    await update.message.reply_text(message)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("fgi", fngCommand))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()