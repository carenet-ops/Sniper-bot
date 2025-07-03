import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ['BOT_TOKEN']
AUTH_PASSWORD = "sniper@321"
authenticated_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to Sniper Bot. Please authenticate using /auth <password>')

async def auth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    try:
        password = context.args[0]
        if password == AUTH_PASSWORD:
            authenticated_users.add(user_id)
            await update.message.reply_text("✅ Access granted. Sniper mode active.")
        else:
            await update.message.reply_text("❌ Incorrect password. Access denied.")
    except IndexError:
        await update.message.reply_text("❗ Usage: /auth <password>")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in authenticated_users:
        await update.message.reply_text("🔒 Please authenticate first using /auth <password>")
        return
    await update.message.reply_text("📊 SONAMLTD Status:\nPrice: ₹XX.XX\nVolume: XXXX\nSignal: 📈 Possible breakout")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in authenticated_users:
        await update.message.reply_text("🔒 Please authenticate first using /auth <password>")
        return
    await update.message.reply_text("🔥 Today's breakout stocks:\n- SONAMLTD\n- XYZCO\n- ABCIND")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("auth", auth))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("now", now))
    app.run_polling()
