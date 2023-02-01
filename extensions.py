import requests
import json
from config import currency


# Обработчик исключений
class APIException (Exception):
    pass


# Конвертор валют
class CurrConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # введенные валюты равны
        if base == quote:
            raise APIException(f'Перевод не нужен: {base} = {base}')
        # введены валюты не из списка
        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Неизвестная валюта {base}\nКоманда /values - справочник валют')
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Неизвестная валюта {quote}\nКоманда /values - справочник валют')
        # 3-ий параметр - не число
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"{amount} - некорректная сумма для конвертации. Введите число")

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')

        cost = float(json.loads(r.content)[currency[quote]])

        return cost * amount
