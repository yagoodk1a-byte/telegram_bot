import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Вставь сюда токен от BotFather в кавычках
import os
TOKEN = os.environ.get("8478581408:AAH0OGhkMnqUh_MvkBsGZk6vYhzWfyNHolk")

from flask import Flask
from threading import Thread

app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is running!"

def run():
    app_flask.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Кнопки выбора времени дня
keyboard = [["Утро", "День", "Ночь"]]
keyboard = InlineKeyboardMarkup()
menu_1 = InlineKeyboardButton(text='Утро', callback_data="menu_1")
menu_2 = InlineKeyboardButton(text='День', callback_data="menu_2")
menu_3 = InlineKeyboardButton(text='Ночь', callback_data="menu_3")
keyboard.add(menu_1, menu_2, menu_3)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь сообщение с числами.",
        reply_markup=markup
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    @dp.callback_query_handler(text_contains='menu_'):
    if call.data and call.data.startswith("menu_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        if code == 1:
            await call.message.edit_text('Утро', reply_markup=keyboard)
        if code == 2:
            await call.message.edit_text('День', reply_markup=keyboard)
        if code == 3:
            await call.message.edit_text('Ночь', reply_markup=keyboard)
        else:
            await bot.answer_callback_query(call.id)

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
keep_alive()
restart=always()
app.run_polling()






