
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang='ar' dir='rtl'>
    <head>
        <meta charset='UTF-8'>
        <title>🤖 بوت تعلّم</title>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <style>
            body { font-family: Tahoma, sans-serif; background: #f2f2f2; color: #333; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 80px auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 0 20px rgba(0,0,0,0.1); text-align: center; }
            h1 { color: #2e86de; }
            p { font-size: 18px; line-height: 1.8; }
            .btn { display: inline-block; margin-top: 25px; padding: 12px 24px; background-color: #2e86de; color: white; font-size: 18px; border-radius: 6px; text-decoration: none; }
            .btn:hover { background-color: #1c5f9c; }
            .footer { margin-top: 40px; font-size: 14px; color: #888; }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>🤖 بوت تعلّم</h1>
            <p>مساعد ذكي متفاعل وفهمان، يشتغل 24 ساعة على الخاص أو في القروبات.</p>
            <p>اسأله، اطلب منه، خله يساعدك في الوقت أو الشرح أو حتى الترفيه.</p>
            <p><strong>صنعه محمد (سنابه: <a href='https://www.snapchat.com/add/im7des' target='_blank'>im7des</a>)</strong></p>
            <a class='btn' href='https://t.me/T3llm_bot' target='_blank'>🚀 جرّب البوت الآن</a>
            <div class='footer'>© 2025 جميع الحقوق محفوظة</div>
        </div>
    </body>
    </html>
    """

def run_flask():
    app.run(host="0.0.0.0", port=3000)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "مرحبًا بك في 🤖 *بوت تعلّم*!
"
        "أنا مساعد ذكي أجاوبك بسرعة وفهم، وأسلوبي طبيعي.
"
        "صنعني محمد (سنابه: @im7des).
"
        "اكتب لي أي شيء يخطر ببالك!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وودود تتحدث بالعربية وتفهم السياق وترد بشكل طبيعي."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[❌] خطأ في OpenAI:", e)
        return "فيه مشكلة مؤقتة. حاول مرة ثانية."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await asyncio.to_thread(ask_gpt, user_message)
    await update.message.reply_text(reply)

def main():
    Thread(target=run_flask).start()
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت شغّال الآن 24/7")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
