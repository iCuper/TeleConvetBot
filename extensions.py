import configparser
import json
import requests


config = configparser.ConfigParser()
config.read('config.ini', encoding='UTF-8')

TOKEN = config["Telegram"]["TOKEN"]
value_dict = config["Keys"]


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        value_1, value_2, summa = base, quote, amount
        if base == quote:
            raise APIException('Нельзя конвертировать одну валюту')
        try:
            value_1_sym = value_dict[base]
        except KeyError:
            raise APIException(f'Не удалось найти валюту {base} в справочнике /values')
        try:
            value_2_sym = value_dict[quote]
        except KeyError:
            raise APIException(f'Не удалось найти валюту {quote} в справочнике /values')
        try:
            summa = float(summa)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {summa}\n Обратите внимание на знак плавающей точки')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={value_1_sym}&tsyms={value_2_sym}')
        json_obj = json.loads(r.content)[value_dict[value_2]]
        return json_obj


