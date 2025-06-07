import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# إعداد OpenRouter مع Claude 3 Haiku
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد سيرفر Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت شغّال! هذه صفحة Flask الأساسية."

def run_flask():
    app.run(host="0.0.0.0", port=3000)

# رسالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🚀 تلقى /start")
    await update.message.reply_text("👋 أهلًا بك في بوت تعلّم! أرسل لي أي رسالة بالعربي.")

# توليد الرد
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تجيب بالعربية بسرعة وبوضوح."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ خطأ في الذكاء:", e)
        return "فيه مشكلة مؤقتة في الذكاء، جرب بعد شوي."

# الرد على أي رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_type = update.message.chat.type
        user_text = update.message.text
        print(f"📩 رسالة من: {chat_type} | النص: {user_text}")

        if chat_type == "private":
            intro = "مرحبًا بك في الخاص 🌟، ارسل سؤالك!"
        else:
            intro = f"رد ذكي من تعلّم 🤖:"

        reply = await asyncio.to_thread(generate_response, user_text)
        await update.message.reply_text(f"{intro}\n\n{reply}")
    except Exception as e:
        print("❌ خطأ في المعالجة:", e)

# التشغيل
async def main():
    # تشغيل Flask في الخلفية
    Thread(target=run_flask).start()

    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت قيد التشغيل...")
    await app_bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
