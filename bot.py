import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "293951418"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте!\n\n"
        "Напишите ваш вопрос или запрос на консультацию.\n\n"
        "Если консультация по натальной карте — укажите дату, время и город рождения."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"📩 Новое обращение\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'нет'}\n"
            f"User ID: {user.id}\n\n"
            f"Сообщение:\n{text}"
        ),
    )

    await update.message.reply_text(
        "Спасибо 🙏\n\n"
        "Ваше сообщение получено.\n"
        "Сергей ответит вам лично."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Consultation bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()