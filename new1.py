
import re
import telebot

bot=telebot.TeleBot("8358575962:AAFscZFM5pElS0AWZs_1kBZFnH-NyLwf034")

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, можешь отправить мне любое сообщение с текстом и числами, я все посчитаю!")


@bot.message_handler(func=lambda message: message.text and message.text.lower() == "привет")
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, можешь отправить мне любое сообщение с текстом и числами, я все посчитаю!")



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    # Ищем все целые и дробные числа (включая отрицательные)
    numbers = re.findall(r'-?\d+\.?\d*', text)

    # Если чисел нет
    if not numbers:
        bot.reply_to(message, "В сообщении нет чисел)")
        return

    # Преобразуем строки в числа
    numbers = [float(num) for num in numbers]

    positive_sum = sum(num for num in numbers if num > 0)
    negative_sum = sum(num for num in numbers if num < 0)
    total_sum = positive_sum + negative_sum

    response = (
        f"Сумма положительных: {positive_sum}\n"
        f"Сумма отрицательных: {negative_sum}\n"
        f"Итого: {total_sum}"
    )

    bot.reply_to(message, response)


bot.polling(none_stop=True)
