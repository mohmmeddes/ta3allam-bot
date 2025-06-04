import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "صديقي"
    await update.message.reply_text(
        f"مرحباً بك في بوت *تعلَّم 🤖*!
"
        f"أنا هنا أساعدك وأذكّرك بأشيائك المهمة ✨
"
        f"أرسل لي أي شيء تبيه، وأنا أرتبه لك.

"
        f"البوت هذا من تصميم محمد 👨🏻‍💻 (سنابه 👻 im7des)"
    )

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()