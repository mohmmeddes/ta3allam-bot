import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import asyncio

# جلب القيم من Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# إعداد OpenRouter مع Claude 3 Haiku
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# إعداد واجهة Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>تعلم - Telegram Bot</title></head>
    <body style="text-align:center; font-family:Tahoma;">
        <h1>🤖 مرحبًا بك في بوت <span style='color:#0077cc;'>تعلّم</span></h1>
        <p>سهل وسريع، يفهمك ويجاوبك بالعربي ✅</p>
        <a href="https://t.me/T3llm_bot" style="font-size:20px; color:#0077cc;">اضغط هنا للدخول للبوت</a>
        <br><br>
        <p>📸 تابعني على سناب:</p>
        <img src="https://snapchat.com/add/im7des/qr" alt="Snapcode" width="180">
        <p>@im7des</p>
    </body>
    </html>
    """

def run_flask():
    app.run(host="0.0.0.0", port=3000)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلًا بك في بوت تعلّم! اسألني أي شيء بالعربي.")

# توليد رد من Claude 3 Haiku
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="anthropic/claude-3-haiku",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي باللغة العربية، تجاوب بسرعة، وبلغة طبيعية وسهلة."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error:", e)
        return "فيه مشكلة مؤقتة، حاول بعد شوي."

# التعامل مع الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = await asyncio.to_thread(generate_response, user_input)
    await update.message.reply_text(reply)

# تشغيل البوت والسيرفر
async def main():
    Thread(target=run_flask).start()
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت شغال...")
    await bot.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
