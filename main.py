
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import asyncio

# مفاتيح البيئة
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_URL = "https://ta3allam-bot.onrender.com"

# إعداد OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = "مرحباً بك في بوت تعلّم 🤖! اسأل أي شيء، وأنا أجاوبك بذكاء. البوت من تطوير محمد - سنابي: im7des"
    await update.message.reply_text(welcome)

# الرد الذكي من Mistral
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي تتحدث العربية وتفهم نبرة المستخدم وترد بسرعة ووضوح."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error:", e)
        return "حصل خطأ مؤقت، جرب بعد شوي."

# استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = "مرحباً بك في بوت تعلّم 🤖! اسأل أي شيء، وأنا أجاوبك بذكاء. البوت من تطوير محمد - سنابي: im7des"
    await update.message.reply_text(intro)

    user_text = update.message.text
    reply = await asyncio.to_thread(generate_response, user_text)
    await update.message.reply_text(reply)

# نقطة الويب هوك
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(app_bot.process_update(update))
    return "ok"

@app.route('/')
def home():
    return 'بوت تعلّم شغال ✅'

# تعيين الويب هوك
async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

if __name__ == "__main__":
    app_bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=3000)
