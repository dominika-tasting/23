import telebot
from config import currency, TOKEN
from extensions import APIException, CurrConverter

bot = telebot.TeleBot(TOKEN)


# Команды /start и /help
@bot.message_handler(commands=["start", "help"])
def bot_help(message):
    text = "Здравствуйте! Я бот-конвертер валют.\n\
Чтобы начать работу, введите команду:\n<имя валюты> <в какую валюту перевести> <сумма>\n\n \
Команды работы с ботом:\n /help - помощь\n /values - список доступных валют"
    bot.reply_to(message, text)


# Команда /values - вывод списка доступных валют
@bot.message_handler(commands=["values"])
def bot_values(message):
    text = "Доступные валюты"
    for i, curr in enumerate(currency.keys()):
        text = f"\n {i + 1}. ".join((text, curr))
    bot.reply_to(message, text)


# Команда вывода стоимости валюты <имя валюты> <в какую валюту перевести> <сумма>
@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Для конвертации валют нужно указать 3 параметра.\nКоманда /help - подсказка')

        base, quote, amount = values
        curr_total = CurrConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка бота, не удалось выполнить команду :(\n{e}')
    else:
        text = f"{amount} {base} = {round(curr_total, 2)} {quote}"

        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
