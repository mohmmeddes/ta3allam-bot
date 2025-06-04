
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

# مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد OpenAI
openai.api_key = OPENAI_API_KEY

# Flask لتشغيل السيرفر
app = Flask(__name__)

@app.route('/')
def home():
    return open("index.html", encoding="utf-8").read()

def run():
    app.run(host="0.0.0.0", port=3000)

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك في بوت تعلّم! اسألني أي شيء، وأنا أساعدك 🤖")

# الرد التلقائي باستخدام GPT
def chat_reply(prompt):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تتحدث العربية بطلاقة."},
                {"role": "user", "content": prompt}
            ]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print("[❌]", e)
        return "صار خطأ، جرب مرة ثانية."

# التعامل مع الرسائل النصية
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = await asyncio.to_thread(chat_reply, user_msg)
    await update.message.reply_text(reply)

# تشغيل البوت
def main():
    Thread(target=run).start()
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
