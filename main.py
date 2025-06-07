import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import openai

# المفاتيح من Render مباشرة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("📌 إعداد المفاتيح...")

# إعداد OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def home():
    print("🌐 زيارة لصفحة Flask")
    return "✅ البوت شغّال! هذه صفحة Flask الأساسية."

def run_flask():
    print("🚀 تشغيل Flask...")
    app.run(host="0.0.0.0", port=3000)

# رد /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"💬 أمر /start من: {update.effective_user.first_name}")
    await update.message.reply_text("👋 أهلًا بك! اسألني أي شيء بالعربي.")

# الرد الذكي
def generate_response(prompt):
    print(f"🧠 طلب من الذكاء الاصطناعي: {prompt}")
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية، تجاوب بسرعة ووضوح وتفهم السياق."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        print(f"✅ رد الذكاء الاصطناعي: {answer}")
        return answer
    except Exception as e:
        print(f"❌ خطأ من OpenRouter: {e}")
        return "حصل خطأ، حاول مرة ثانية."

# استقبال رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user = update.effective_user.first_name
    print(f"📩 رسالة من {user}: {user_text}")
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

# تشغيل البوت
async def start_bot():
    print("🤖 تشغيل بوت تليجرام...")
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت جاهز ويبدأ polling...")
    await app_bot.run_polling()

# تشغيل الكل
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(start_bot())
