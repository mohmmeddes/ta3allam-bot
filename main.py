
import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>بوت تعلّم 🤖</title>
        <style>
            body { font-family: Tahoma, sans-serif; background-color: #f4f6f9; text-align: center; padding: 40px; }
            .container { max-width: 600px; background: #fff; margin: auto; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; }
            h1 { color: #2e86de; }
            .btn { background: #2e86de; color: white; padding: 12px 20px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 بوت تعلّم</h1>
            <p>شغال 24 ساعة باستخدام GPT-4 Turbo من OpenRouter</p>
            <a class="btn" href="https://t.me/T3llm_bot" target="_blank">ابدأ المحادثة في تليجرام</a>
        </div>
    </body>
    </html>
    '''

def run_flask():
    app.run(host="0.0.0.0", port=3000)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في بوت تعلّم 🤖! اسأل أي شيء، وأنا أجاوبك بذكاء.")

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تتحدث العربية وترد بأسلوب واضح وبسيط."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error:", e)
        return "فيه مشكلة مؤقتة، جرب بعد شوي."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

def main():
    Thread(target=run_flask).start()
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
