import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "293951418"))

CHANNEL_URL = "https://t.me/vedascope"
YOUTUBE_URL = "https://youtube.com/@vedascope"
VK_URL = "https://vk.com/vedascope"

FORECASTS_DIR = Path("forecasts")

ZODIAC_SIGNS = {
    "aries": ("♈ Овен", "aries.txt"),
    "taurus": ("♉ Телец", "taurus.txt"),
    "gemini": ("♊ Близнецы", "gemini.txt"),
    "cancer": ("♋ Рак", "cancer.txt"),
    "leo": ("♌ Лев", "leo.txt"),
    "virgo": ("♍ Дева", "virgo.txt"),
    "libra": ("♎ Весы", "libra.txt"),
    "scorpio": ("♏ Скорпион", "scorpio.txt"),
    "sagittarius": ("♐ Стрелец", "sagittarius.txt"),
    "capricorn": ("♑ Козерог", "capricorn.txt"),
    "aquarius": ("♒ Водолей", "aquarius.txt"),
    "pisces": ("♓ Рыбы", "pisces.txt"),
}

FOOTER_TEXT = """
━━━━━━━━━━━━━━

🔮 Хотите узнать свой персональный прогноз?

Общий прогноз учитывает только транзиты.

В вашей карте также работают:
• периоды — даши
• положение планет
• йоги
• сила домов
• личные задачи года

Поэтому личный прогноз всегда точнее общего.
"""


def main_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Календарь Панчанга", url="https://vedascope.ru/panchanga")],
            [InlineKeyboardButton("Ближайшие Джйотиш-мероприятия", url="https://vedascope.ru/#events")],
            [InlineKeyboardButton("Запись на консультацию", callback_data="consultation")],
            [InlineKeyboardButton("Получить бесплатный прогноз на год", callback_data="free_forecast")],
            [
                InlineKeyboardButton("Мы на YouTube", url="https://www.youtube.com/@vedascope"),
                InlineKeyboardButton("Мы на VK", url="https://vk.com/vedascope"),
            ],
            [InlineKeyboardButton("Подписаться на @vedascope", url=CHANNEL_URL)],
        ]
    )


def zodiac_menu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("♈ Овен", callback_data="forecast:aries"),
                InlineKeyboardButton("♉ Телец", callback_data="forecast:taurus"),
                InlineKeyboardButton("♊ Близнецы", callback_data="forecast:gemini"),
            ],
            [
                InlineKeyboardButton("♋ Рак", callback_data="forecast:cancer"),
                InlineKeyboardButton("♌ Лев", callback_data="forecast:leo"),
                InlineKeyboardButton("♍ Дева", callback_data="forecast:virgo"),
            ],
            [
                InlineKeyboardButton("♎ Весы", callback_data="forecast:libra"),
                InlineKeyboardButton("♏ Скорпион", callback_data="forecast:scorpio"),
                InlineKeyboardButton("♐ Стрелец", callback_data="forecast:sagittarius"),
            ],
            [
                InlineKeyboardButton("♑ Козерог", callback_data="forecast:capricorn"),
                InlineKeyboardButton("♒ Водолей", callback_data="forecast:aquarius"),
                InlineKeyboardButton("♓ Рыбы", callback_data="forecast:pisces"),
            ],
        ]
    )


def forecast_footer_menu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔮 Записаться на консультацию", callback_data="consultation")],
            [InlineKeyboardButton("📅 Построить свою карту", callback_data="panchanga")],
            [
                InlineKeyboardButton("📢 Telegram", url=CHANNEL_URL),
                InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_URL),
            ],
            [InlineKeyboardButton("📘 VK", url=VK_URL)],
        ]
    )


def load_forecast(sign_key: str) -> str:
    if sign_key not in ZODIAC_SIGNS:
        return "Прогноз для этого знака пока не найден."

    _, filename = ZODIAC_SIGNS[sign_key]
    path = FORECASTS_DIR / filename

    if not path.exists():
        return "Прогноз для этого знака пока не добавлен."

    return path.read_text(encoding="utf-8").strip()


async def send_long_text(message, text: str):
    max_length = 3900

    if len(text) <= max_length:
        await message.reply_text(text)
        return

    parts = []
    current = ""

    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) + 2 <= max_length:
            current += paragraph + "\n\n"
        else:
            parts.append(current.strip())
            current = paragraph + "\n\n"

    if current.strip():
        parts.append(current.strip())

    for part in parts:
        await message.reply_text(part)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать на vedascope — исследовательский проект для тех, "
        "кто хочет глубже понять себя с помощью Джйотиш.\n\n"
        "Здесь вы найдете сервисы для астрологов, обучающие материалы, "
        "полезные ссылки, живую базу знаний, а также мероприятия "
        "Джйотиш-сообщества.\n\n"
        "Присоединяйтесь.\n\n"
        "Выберите, с чего начать:",
        reply_markup=main_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    if query.data == "consultation":
        await query.message.reply_text(
            "Для записи на консультацию напишите одним сообщением:\n\n"
            "• дату рождения\n"
            "• точное время рождения\n"
            "• город рождения\n"
            "• ваш вопрос или тему разбора\n\n"
            "После этого Сергей свяжется с вами лично."
        )

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                "🔔 Пользователь нажал «Запись на консультацию»\n\n"
                f"Имя: {user.first_name}\n"
                f"Username: @{user.username if user.username else 'нет'}\n"
                f"User ID: {user.id}"
            ),
        )

    if query.data == "free_forecast":
        await query.message.reply_text(
            "🎁 Бесплатный прогноз на 2026 год\n\n"
            "Выберите свой знак Луны по Джйотиш.\n\n"
            "Если вы его не знаете — постройте бесплатно свою карту в нашем сервисе.",
            reply_markup=zodiac_menu(),
        )

    if query.data == "panchanga":
        await query.message.reply_text(
            "📅 Панчанга уже доступна:\n\nhttps://vedascope.ru/panchanga\n\n"
            "Сейчас сервис находится на этапе финального тестирования."
        )

    if query.data.startswith("forecast:"):
        sign_key = query.data.split(":", 1)[1]
        sign_name = ZODIAC_SIGNS.get(sign_key, ("", ""))[0]

        await query.message.reply_text(f"⏳ Загружаю прогноз: {sign_name}")

        forecast = load_forecast(sign_key)

        await send_long_text(query.message, forecast)

        await query.message.reply_text(
            FOOTER_TEXT,
            reply_markup=forecast_footer_menu(),
        )

        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                "🎁 Пользователь получил бесплатный прогноз\n\n"
                f"Знак: {sign_name}\n"
                f"Имя: {user.first_name}\n"
                f"Username: @{user.username if user.username else 'нет'}\n"
                f"User ID: {user.id}"
            ),
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "📩 Новое обращение\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'нет'}\n"
            f"User ID: {user.id}\n\n"
            f"Сообщение:\n{text}"
        ),
    )

    await update.message.reply_text(
        "Спасибо 🙏\n\n"
        "Ваше сообщение получено.\n"
        "Сергей ответит вам лично.",
        reply_markup=main_menu(),
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Consultation bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()