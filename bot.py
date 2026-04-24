import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip().replace("=", "").replace(" ", "")
OPENROUTER_KEY = os.environ["OPENROUTER_API_KEY"].strip()
ALLOWED_USER = int(os.environ["TELEGRAM_ALLOWED_USERS"].strip().lstrip("="))

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER:
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
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
