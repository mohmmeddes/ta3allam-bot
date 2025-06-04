import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import asyncio
from threading import Thread

# إعداد المتغيرات
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد OpenAI الرسمي
openai.api_key = OPENAI_API_KEY
openai.api_base = "https://api.openai.com/v1"

# إعداد Flask
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return '''
    <meta charset="UTF-8">
    <h2>بوت تعلم شغّال ✅</h2>
    <p>تم صنعه بواسطة <strong>محمد</strong> - سناب: <strong>im7des</strong></p>
    <p>جرّب البوت على <a href="https://t.me/T3llm_bot">تليجرام</a></p>
    '''

# رسالة ترحيب أولى
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في بوت تعلّم 🤖! اسأل أي شيء، وأنا أجاوبك بذكاء. 
تم تطويري بواسطة محمد - سنابه: im7des")

# توليد رد باستخدام OpenAI
def generate_reply(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وسريع، تتحدث العربية بطلاقة وترد بأدب وسرعة."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[خطأ GPT]:", e)
        return "فيه مشكلة مؤقتة، جرب بعد شوي."

# التعامل مع أي رسالة نصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await asyncio.to_thread(generate_reply, user_message)
    await update.message.reply_text(reply)

# تشغيل Flask والبوت معاً
def run():
    flask_app.run(host="0.0.0.0", port=3000)

def main():
    Thread(target=run).start()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن.")
    app.run_polling()

if __name__ == "__main__":
    main()
