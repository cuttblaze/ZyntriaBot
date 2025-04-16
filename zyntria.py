from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") # TOKEN

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛰  Welcome to ZYNTRIA.\n\n"
        "We design collectible figures forged from data and resin — artifacts of imagined worlds and digital craftsmanship.\n\n"
        "Choose your directive:\n"
        "/about – What is ZYNTRIA\n"
        "/early – You're early, stay updated\n"
        "/socials – Connect across the grid"
    )

# Команда /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍  ZYNTRIA creates hyper-detailed 3D-printed figures inspired by cyberpunk, sci-fi and digital mythology.\n\n"
        "Born in 2025. Printed in Switzerland.\n"
    )

# Команда /socials
async def socials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐  CONNECT WITH HQ:\n\n"
        "[🌍 Website - in Progress](In Progress)\n"
        "[📸 Instagram](https://www.instagram.com/zyntria.lab/)\n"
        "[🎥 TikTok](https://www.tiktok.com/@zyntria.lab)\n"
        "[🕊 X](https://x.com/ZyntriaLab)",
        parse_mode=ParseMode.MARKDOWN_V2
    )

# Команда /early
async def early(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏳ You're to early.\n\n"
        "Track our progress and upcoming drops via socials."
    )

# Команда /override (пасхалка)
async def override(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛑 Access denied. Only Syndicate-level operatives may run internal overrides."
    )

# Запуск приложения
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("socials", socials))
    app.add_handler(CommandHandler("early", early))
    app.add_handler(CommandHandler("override", override))

    print("ZYNTRIA Bot is now online.")
    app.run_polling()
