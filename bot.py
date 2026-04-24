import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().replace("=", "").replace(" ", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
ALLOWED_USER = int(os.environ.get("TELEGRAM_ALLOWED_USERS", "0").strip().lstrip("="))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    print(f"START - User ID: {update.effective_user.id}, ALLOWED: {ALLOWED_USER}")
    if update.effective_user.id != ALLOWED_USER:
        await update.message.reply_text("غير مصرح لك.")
        return
    await update.message.reply_text("مرحباً! أنا Hermes، كيف يمكنني مساعدتك؟")

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    print(f"MSG - User ID: {update.effective_user.id}, ALLOWED: {ALLOWED_USER}")
    if update.effective_user.id != ALLOWED_USER:
        await update.message.reply_text("غير مصرح لك.")
        return
    msg = update.message.text
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [{"role": "user", "content": msg}]
        }
    )
    reply = r.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling(drop_pending_updates=True)
