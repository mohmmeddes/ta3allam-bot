from flask import Flask, request, render_template
import asyncio
from telegram import Update, __version__ as TG_VER
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://ta3allam-bot-1.onrender.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في بوت تعلّم! 👋")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = "مرحبًا بك في بوت تعلّم! 👋 اسأل أي شيء، وأنا أجابك بذكاء. البوت من تطوير محمد - سنابي: im7des"
    await update.message.reply_text(intro)

    user_text = update.message.text
    reply = f"أنت قلت: {user_text}"
    await update.message.reply_text(reply)

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(app_bot.process_update(update))
    return "ok", 200

@app.route("/")
def home():
    return render_template("index.html")

WEBHOOK_URL = "https://ta3allam-bot-1.onrender.com"

async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    asyncio.run(app_bot.initialize())

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=3000)
