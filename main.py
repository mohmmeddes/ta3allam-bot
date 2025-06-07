import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

# مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# إعداد OpenRouter مع GPT-4 Turbo
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# سيرفر Flask لتشغيل Replit + UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return open("index.html", "r", encoding="utf-8").read()

def run_flask():
    app.run(host="0.0.0.0", port=3000, debug=False)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك في بوت تعلّم! اسألني أي شيء بالعربي.")

# رد من GPT-4 Turbo
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تتحدث العربية بطلاقة وتفهم نبرة المستخدم وترد بسرعة ووضوح."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
