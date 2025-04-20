import os
import re
import json
import asyncio
from dotenv import load_dotenv
from telegram.ext import MessageHandler, filters, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Установка команд
async def setup_commands(application):
    commands = [
        BotCommand("start", "Launch the Zyntria interface"),
        BotCommand("early", "Join as early user"),
    ]
    await application.bot.set_my_commands(commands)

def escape_md(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 About", callback_data="about")],
        [InlineKeyboardButton("🛰 Socials", callback_data="socials")],
        [InlineKeyboardButton("⚙️ Create Figure", callback_data="create")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "🛰 *ZYNTRIA* creates hyper-detailed 3D-printed figures inspired by cyberpunk, sci-fi and digital mythology.",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "🛰 *ZYNTRIA* creates hyper-detailed 3D-printed figures inspired by cyberpunk, sci-fi and digital mythology.",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

# Обработка главных кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text(
            "🔍  ZYNTRIA creates hyper-detailed 3D-printed figures inspired by cyberpunk, sci-fi and digital mythology.\n\n"
            "Born in 2025. Printed in Switzerland."
        )
    elif query.data == "socials":
        message = (
            "🌐  CONNECT WITH HQ:\n\n"
            "[🌍 Website \\- in Progress](https://zyntria.com)\n"
            "[📸 Instagram](https://www.instagram.com/zyntria.lab/)\n"
            "[🎥 TikTok](https://www.tiktok.com/@zyntria.lab)\n"
            "[🕊 X](https://x.com/ZyntriaLab)"
        )
        await query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    elif query.data == "create":
        await query.edit_message_text("⚙️ Create feature is not available yet.")

# STEP 1: Start figure creation
async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cyberpunk", callback_data="style_Cyberpunk")],
        [InlineKeyboardButton("Sci-Fi", callback_data="style_Sci-Fi")],
        [InlineKeyboardButton("Mythic", callback_data="style_Mythic")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🧬 Choose your figure style:",
        reply_markup=reply_markup
    )

# STEP 2: Type selection and processing
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data.startswith("style_"):
        style = data.split("_")[1]
        context.user_data["style"] = style

        keyboard = [
            [InlineKeyboardButton("Humanoid", callback_data="type_Humanoid")],
            [InlineKeyboardButton("Mech", callback_data="type_Mech")],
            [InlineKeyboardButton("Creature", callback_data="type_Creature")]
        ]
        await query.edit_message_text(
            f"✅ Style selected: *{style}*\n\nChoose figure type:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("type_"):
        ftype = data.split("_")[1]
        context.user_data["type"] = ftype

        keyboard = [
            [InlineKeyboardButton("Matte Black", callback_data="finish_Matte Black")],
            [InlineKeyboardButton("Silver Chrome", callback_data="finish_Silver Chrome")],
            [InlineKeyboardButton("Neon Blend", callback_data="finish_Neon Blend")]
        ]
        await query.edit_message_text(
            f"✅ Type selected: *{ftype}*\n\nChoose finish:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("finish_"):
        finish = data.split("_")[1]
        context.user_data["finish"] = finish

        style = context.user_data.get("style", "Unknown")
        ftype = context.user_data.get("type", "Unknown")

        await query.edit_message_text(
            f"🧩 *Figure Assembled!*\n\n"
            f"Style: `{style}`\n"
            f"Type: `{ftype}`\n"
            f"Finish: `{finish}`\n\n"
            f"Thank you for using the ZYNTRIA Figure Generator.",
            parse_mode=ParseMode.MARKDOWN
        )

# ConversationHandler для раннего доступа
USERNAME, EMAIL, EXPECTATION, CONFIRM = range(4)

async def early_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Enter your Telegram username (start with @):")
    return USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    if not username.startswith("@"):
        await update.message.reply_text("❌ Please enter a valid Telegram username starting with '@'. Try again:")
        return USERNAME

    context.user_data["username"] = username
    await update.message.reply_text("📧 Enter your email address:")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    if "@" not in email or "." not in email:
        await update.message.reply_text("❌ That doesn't look like a valid email. Try again:")
        return EMAIL

    context.user_data["email"] = email
    await update.message.reply_text("💬 What do you expect from Zyntria? (Answer in English)")
    return EXPECTATION

async def get_expectation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expectation = update.message.text.strip()
    context.user_data["expectation"] = expectation

    summary = (
        "✅ Please confirm your info:\n\n"
        f"👤 Username: `{context.user_data['username']}`\n"
        f"📧 Email: `{context.user_data['email']}`\n"
        f"💬 Expectation: _{context.user_data['expectation']}_\n\n"
        "Type `yes` to confirm or `no` to cancel."
    )

    await update.message.reply_text(summary, parse_mode=ParseMode.MARKDOWN)
    return CONFIRM

async def confirm_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "yes":
        data = {
            "username": context.user_data["username"],
            "email": context.user_data["email"],
            "expectation": context.user_data["expectation"]
        }

        with open("early_users.json", "a") as f:
            f.write(json.dumps(data) + "\n")

        await update.message.reply_text("✅ You're on the early list. Stay tuned!")
    else:
        await update.message.reply_text("❌ Submission canceled.")

    return ConversationHandler.END

# Пасхалка /override
async def override(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛑 Access denied. Only Syndicate-level operatives may run internal overrides.")

# MAIN ЗАПУСК
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    await setup_commands(app)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("override", override))
    app.add_handler(CallbackQueryHandler(create, pattern="^create$"))
    app.add_handler(CallbackQueryHandler(handle_callback, pattern="^(style_|type_|finish_)"))
    app.add_handler(CallbackQueryHandler(button_callback))

    early_conv = ConversationHandler(
        entry_points=[CommandHandler("early", early_start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            EXPECTATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_expectation)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_submission)],
        },
        fallbacks=[],
    )
    app.add_handler(early_conv)

    print("ZYNTRIA Bot is now online.")
    await app.run_polling()


if __name__ == '__main__':
    import asyncio


    async def start_bot():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        await setup_commands(app)

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("override", override))
        app.add_handler(CallbackQueryHandler(create, pattern="^create$"))
        app.add_handler(CallbackQueryHandler(handle_callback, pattern="^(style_|type_|finish_)"))
        app.add_handler(CallbackQueryHandler(button_callback))

        early_conv = ConversationHandler(
            entry_points=[CommandHandler("early", early_start)],
            states={
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
                EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
                EXPECTATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_expectation)],
                CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_submission)],
            },
            fallbacks=[],
        )
        app.add_handler(early_conv)

        print("✅ ZYNTRIA Bot is running.")
        await app.run_polling()


    try:
        asyncio.get_event_loop().run_until_complete(start_bot())
    except RuntimeError as e:
        print(f"❌ Event loop error: {e}")
        # Альтернативный запуск для среды с уже активным loop
        loop = asyncio.get_event_loop()
        loop.create_task(start_bot())
        loop.run_forever()
