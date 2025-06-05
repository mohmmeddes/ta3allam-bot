from flask import Flask, request, render_template
import asyncio
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://ta3allam-bot-1.onrender.com"


# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = "👋 أهلًا في بوت تعلّم! أنا هنا أساعدك بكل ذكاء، اسألني اللي تبي ✨"
    await update.message.reply_text(welcome)

# الرد على أي رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = "🤖 مرحبًا بك في بوت تعلّم! اسأل أي شيء، وأنا أجتهد بإذن الله أساعدك. البوت من تطوير محمد - سنابي: im7des 👨🏻‍💻"
    await update.message.reply_text(intro)

    user_text = update.message.text
    reply = f"👀 أنت قلت: {user_text}"
    await update.message.reply_text(reply)

# نقطة استقبال Webhook من تليجرام
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    from telegram import Update
    update = Update.de_json(request.get_json(force=True), app.bot)
    asyncio.run(app.bot.process_update(update))
    return "ok", 200

# صفحة الترحيب
@app.route("/")
def home():
    return render_template("index.html")

# المهمة الرئيسية
async def main():
    app.bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    await app.bot.initialize()
    app.bot.add_handler(CommandHandler("start", start))
    app.bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.bot.set_webhook(f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

    app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    asyncio.run(main())
