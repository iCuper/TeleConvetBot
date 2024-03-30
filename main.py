import telebot
from extensions import Converter, value_dict, TOKEN, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Введите запрос следующего вида:\n<ВАЛЮТА 1> <ВАЛЮТА 2> <КОЛЛИЧЕСТВО>')
    bot.send_message(message.chat.id, '<ВАЛЮТА 1> - имя валюты, цену которой необходимо узнать\n<ВАЛЮТА 2> - имя '
                                      'валюты, в которой надо узнать цену первой валюты\n<КОЛИЧЕСТВО> - количество '
                                      'первой валюты')
    bot.send_message(message.chat.id, 'Например: биткоин доллар 0.3241\n/values - список доступных валют')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Доступные валюты:')
    text = '\n'.join(value_dict)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        message_text = message.text.split(' ')
        if len(message_text) != 3:
            raise APIException(f'Некорректный ввод аргументов. Подробнее /start или /help')
        base, quote, amount = message_text
        convert_obj = Converter().get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        total = convert_obj * float(amount)
        bot.send_message(message.chat.id, f'Цена {base} в {quote} = {round(total, 2)}')


bot.polling()
