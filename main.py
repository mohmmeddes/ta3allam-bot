import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

# إعداد مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# إعداد Claude 3 Haiku
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# سيرفر Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h3>✅ البوت شغال - Flask جاهز</h3>"

def run_flask():
    app.run(host="0.0.0.0", port=3000)

# أوامر Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك في بوت تعلّم! اسألني أي شيء بالعربي.")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[❌]", e)
        return f"⚠️ خطأ من الذكاء الاصطناعي:\n{e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print(f"[📥] من المستخدم: {user_text}")
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

async def run_bot():
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت بدأ")
    await app_bot.run_polling()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())