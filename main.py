import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
import openai

# إعداد المفاتيح
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد سيرفر Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغّال! صفحة Flask الأساسية."

def run_flask():
    app.run(host="0.0.0.0", port=3000)

# أوامر تليجرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك! اسألني أي شيء.")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية وتفهم سياق الكلام وترد بوضوح."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error:", e)
        return "حصل خطأ، جرب مرة ثانية."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

# تشغيل البوت
async def run_bot():
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت شغّال الآن واستعد للاستقبال...")
    await app_bot.run_polling()

# التشغيل
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(run_bot())