import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().replace("=", "").replace(" ", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip().replace("=", "").replace(" ", "")
ALLOWED_USER = int(os.environ.get("TELEGRAM_ALLOWED_USERS", "0").strip().lstrip("="))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER:
        return
    await update.message.reply_text("مرحباً! أنا Hermes، كيف يمكنني مساعدتك؟")

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER:
        return
    msg = update.message.text
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [{"role": "user", "content": msg}]
            },
            timeout=30
        )
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"خطأ: {str(e)}"
    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling(drop_pending_updates=True)
