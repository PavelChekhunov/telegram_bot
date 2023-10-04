import telebot
from app_config import BOT_TOKEN
from extension import CurrencyConverter, ConversionException


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_msg(message: telebot.types.Message):
    text = ("Комманда для конвертирования валюты:\n<Имя исходной валюты> "
            "<Имя получаемой валюты> <Количество исходной валюты>\n"
            "Комманда для просмотра доступных валют: /currency или /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=['currency', 'values'])
def currency(message: telebot.types.Message):
    bot.reply_to(message, CurrencyConverter.get_currency_text())


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        text = CurrencyConverter.convert(message.text)
    except ConversionException as ex:
        bot.reply_to(message, f'Ошибка конвертации валюты:\n{ex}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду\n{e}')
    else:
        bot.send_message(message.chat.id, text, parse_mode="HTML")


bot.polling()
