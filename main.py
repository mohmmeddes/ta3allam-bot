import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

# مفاتيح التوكنات من Render (env)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# إعداد OpenRouter مع Claude 3 Haiku
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# Flask لصفحة الترحيب
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>بوت تــعلّم</title>
        <style>
            body { font-family: Arial; text-align: center; padding: 50px; background: #f9f9f9; }
            h1 { color: #4CAF50; }
            p { font-size: 18px; }
            a.button {
                background-color: #4CAF50; color: white; padding: 14px 25px;
                text-align: center; text-decoration: none; display: inline-block;
                border-radius: 5px; font-size: 18px;
            }
        </style>
    </head>
    <body>
        <h1>🎓 مرحبًا بك في بوت <strong>تــعلّم</strong>!</h1>
        <p>اسألني أي شيء وسأساعدك بالعربية ببساطة وسرعة.</p>
        <a class="button" href="https://t.me/T3llm_bot" target="_blank">ابدأ المحادثة مع البوت</a>
        <br><br>
        <img src="https://snapchat.com/add/im7des" alt="سناب شات" width="180" />
        <p>تابعنا على سناب 👻: <strong>@im7des</strong></p>
    </body>
    </html>
    """

def run_flask():
    app.run(host="0.0.0.0", port=3000)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك في بوت تــعلّم! اسألني أي سؤال بالعربية.")

# توليد رد باستخدام Claude 3 Haiku
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي بالعربية تجاوب بسرعة وتفهم السياق."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ خطأ:", e)
        return "فيه مشكلة مؤقتة، جرب بعد شوي."

# رد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

# تشغيل البوت و Flask معًا
async def main():
    Thread(target=run_flask).start()
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت شغال الآن...")
    await app_bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
