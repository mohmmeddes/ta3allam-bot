import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
import openai

# تفعيل اللوقات
logging.basicConfig(
    format='[%(asctime)s] - %(levelname)s - %(message)s',
    level=logging.INFO
)

# مفاتيح التشغيل
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت يعمل! صفحة Flask الأساسية."

def run_flask():
    logging.info("🚀 تشغيل Flask على المنفذ 3000...")
    app.run(host="0.0.0.0", port=3000)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("📩 تم استقبال أمر /start")
    await update.message.reply_text("👋 أهلًا بك! اسألني أي شيء.")

# الذكاء الاصطناعي
def generate_response(prompt):
    logging.info(f"🧠 يتم إرسال السؤال إلى OpenRouter: {prompt}")
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية وتفهم سياق الكلام وترد بوضوح."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        logging.info(f"✅ تم استلام الرد: {reply}")
        return reply
    except Exception as e:
        logging.error(f"❌ خطأ في OpenRouter: {e}")
        return "⚠️ حصل خطأ أثناء توليد الرد. جرب مرة ثانية."

# استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logging.info(f"📥 رسالة جديدة: {user_text}")
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)
    logging.info("📤 تم إرسال الرد بنجاح.")

# تشغيل البوت
async def run_bot():
    logging.info("🤖 بدء تشغيل البوت...")
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("✅ البوت يعمل الآن عبر polling...")
    await app_bot.run_polling()

# التشغيل الكامل
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(run_bot())