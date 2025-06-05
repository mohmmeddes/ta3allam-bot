from flask import Flask, request, render_templateimport asyncio
from telegram import Update

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://ta3allam-bot-1.onrender.com"

app = Flask(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = "مرحبًا بك في بوت تعلّم 🎓! اسأل أي شيء، وأنا أجاوبك بذكاء. البوت من تطوير محمد - سنابي: im7des"
    await update.message.reply_text(intro)

    user_text = update.message.text
    reply = f"سم، وش تبيني أقول لك عن: {user_text}؟"
    await update.message.reply_text(reply)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(app_bot.process_update(update))
    return "ok", 200

@app.route('/')
def home():
    return render_template("index.html")

async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app_bot.add_handler(CommandHandler("start", handle_message))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=3000)
