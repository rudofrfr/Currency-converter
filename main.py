import telebot
from currency_converter import CurrencyConverter
bot = telebot.TeleBot('7934266316:AAGJ7jUtYzB3lTqmoCIuzeCHm9pk5ZoGLbw')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def hello_speech(message):
    bot.send_message(message.chat.id, '''Hi, type down the amountof money you would like to convert
    (eg. Type down "50" if you want to convert 50$)''')
    bot.register_next_step_handler(message, money_input)


def money_input(message):
    global amount
    try:
        amount = int(message.text.strip())
        if amount < 0:
            bot.send_message(message.chat.id, "You cannot convert negative numbers. Try again!")
            bot.register_next_step_handler(message, money_input)
            return
    except Exception as e:
        bot.send_message(message.chat.id, "Something went wrong, please follow the instructions of the bot. Try again!")
        bot.register_next_step_handler(message, money_input)
        return

    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("EUR/USD", callback_data="EUR/USD")
    btn2 = telebot.types.InlineKeyboardButton("USD/EUR", callback_data="USD/EUR")
    btn3 = telebot.types.InlineKeyboardButton("EUR/RUB", callback_data="EUR/RUB")
    btn4 = telebot.types.InlineKeyboardButton("RUB/EUR", callback_data="RUB/EUR")
    btn5 = telebot.types.InlineKeyboardButton("RUB/USD", callback_data="RUB/USD")
    btn6 = telebot.types.InlineKeyboardButton("USD/RUB", callback_data="USD/RUB")
    btn7 = telebot.types.InlineKeyboardButton("Other currencies", callback_data="else")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, "Choose the pairs that you need", reply_markup=markup)


@bot.callback_query_handler(function=lambda call: True)
def reaction(call):
    values = call.data.split("/")
    response = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'The result is {round(response, 2)}. Feel free to use the bot again!')
    bot.register_next_step_handler(call.message, money_input)



bot.polling(non_stop=True)