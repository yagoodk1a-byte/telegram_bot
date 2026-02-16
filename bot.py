import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Вставь сюда токен от BotFather в кавычках
TOKEN = "8478581408:AAH0OGhkMnqUh_MvkBsGZk6vYhzWfyNHolk"

# Кнопки выбора времени дня
keyboard = [["Утро", "День", "Ночь"]]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь сообщение с числами.",
        reply_markup=markup
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Находим ВСЕ числа (включая отрицательные)
    numbers = re.findall(r'-?\d+', text)

    # Превращаем их в числа
    numbers = [int(num) for num in numbers]

    # Отдельно считаем положительные и отрицательные
    positive_sum = sum(num for num in numbers if num > 0)
    negative_sum = sum(num for num in numbers if num < 0)

    total = positive_sum + negative_sum

    await update.message.reply_text(
        f"Сумма положительных: {positive_sum}\n"
        f"Сумма отрицательных: {negative_sum}\n"
        f"Общий итог: {total}"
   )

# Настройка бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
app.run_polling()

