import os
import openai
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد المفاتيح
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# إعداد Claude 3 Haiku عبر OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد صفحة الويب
app = Flask(__name__)

@app.route('/')
def home():
    return open("index.html", "r", encoding="utf-8").read()

def run_web():
    app.run(host="0.0.0.0", port=3000)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك في بوت تعلّم! اسألني أي شيء بالعربي.")

# توليد الرد من Claude
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية، تجاوب بسرعة وتفهم السياق."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[❌]", e)
        return "فيه مشكلة مؤقتة، جرّب بعد شوي."

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

# تشغيل البوت
async def main():
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()
    await bot.updater.idle()

# تشغيل الواجهة + البوت
if __name__ == "__main__":
    Thread(target=run_web).start()
    loop = asyncio.get_event_loop()
    loop.create_task(main())
