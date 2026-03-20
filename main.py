
import re
import telebot

bot = telebot.TeleBot("8358575962:AAFscZFM5pElS0AWZs_1kBZFnH-NyLwf034")

lots = {

# 400
"7/400": [150,100,50],
"10/400": [150,50,50],
"14/400": [200,50,50],
"17/400": [200,150,50],
"20/400": [250,250,50],
"24/400": [250,250,50],
"28/400": [350,300,50],
"33/400": [350,300,50],
"37/400": [350,300,50],
"41/400": [400,400,50],
"42/400": [400,400,50],
"45/400": [400,400,50],
"50/400": [400,400,150],

# 600
"16/600": [200,150,50],
"26/600": [350,300,50],
"36/600": [350,300,50],
"46/600": [400,400,50],

# 1000
"11/1000": [200,150,50],
"15/1000": [150,100,50],
"20/1000": [300,300,50],
"25/1000": [300,300,150],
"30/1000": [300,300,150],
"40/1000": [400,400,150],

# 1500
"17/1500": [200,200,100],
"27/1500": [350,350,150],
"37/1500": [400,400,150],

# 2000
"15/2000": [300,250,50],
"20/2000": [300,300,150],
"25/2000": [300,300,150],
"30/2000": [400,400,150],
"35/2000": [400,400,150],
}


def calculate_chests(text):

    lines = text.split("\n")
    result = []

    for line in lines:

        match = re.search(r'([\d/]+)\s*:\s*(\d+)', line)

        if not match:
            continue

        lot = match.group(1)
        count = int(match.group(2))

        # если написали только номер (например 10)
        if "/" not in lot:
            lot_key = None
            for key in lots:
                if key.startswith(lot + "/"):
                    lot_key = key
                    break
        else:
            lot_key = lot

        if lot_key in lots:

            chests = lots[lot_key]
            multiplied = [x * count for x in chests]

            result.append(
                f"{lot_key}: {count} - {'/'.join(map(str, multiplied))}"
            )

        else:
            result.append(f"{lot}: лот не найден")

    if not result:
        return None

    return "\n".join(result)


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}, теперь я могу считать числа и расписывать лоты!"
    )


@bot.message_handler(func=lambda message: message.text and message.text.lower() == "привет")
def info(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}, отправь числа или лоты."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    text = message.text

    # если есть :
    if ":" in text:

        result = calculate_chests(text)

        if result:
            bot.reply_to(message, result)
            return

    # обычный подсчёт чисел
    numbers = re.findall(r'-?\d+\.?\d*', text)

    if not numbers:
        bot.reply_to(message, "В сообщении нет чисел)")
        return

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
