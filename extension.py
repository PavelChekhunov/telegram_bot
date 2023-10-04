import json
import requests


currencies = {
    'РУБЛЬ': 'RUB',
    'RUB': 'RUB',
    'ЕВРО': 'EUR',
    'EUR': 'EUR',
    'ДОЛЛАР_США': 'USD',
    'USD': 'USD',
    'КАНАДСКИЙ_ДОЛЛАР': 'CAD',
    'CAD': 'CAD',
    'ЮАНЬ': 'CNY',
    'CNY': 'CNY',
    'ШВЕЙЦАРСКИЙ_ФРАНК': 'CHF',
    'CHF': 'CHF'
}


class ConversionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_currency_text():
        text = "Доступные валюты:\n" + '\n'.join(currencies)
        text += "\n\nВводить можно либо полное название валюты, либо код валюты (строка ниже названия)."
        return text

    @staticmethod
    def convert(text: str):
        values = text.split(' ')
        if len(values) != 3:
            raise ConversionException('Неверное количество параметров комманды!')

        cur_from, cur_to, qty = values
        # cur_from_code, cur_to_code, amount = '', '', 1
        try:
            cur_from_code = currencies[cur_from.upper()]
        except KeyError:
            raise ConversionException(f'Валюта {cur_from} не представлена в списке допустимых валют.')
        try:
            cur_to_code = currencies[cur_to.upper()]
        except KeyError:
            raise ConversionException(f'Валюта {cur_to} не представлена в списке допустимых валют.')
        try:
            amount = int(qty)
        except ValueError:
            raise ConversionException(f'Количество {cur_from} не является допустимым значением.')
        if cur_to_code == cur_from_code:
            raise ConversionException(f'Нельзя конвертировать валюту {cur_from_code} в саму себя')

        uri = f'https://min-api.cryptocompare.com/data/price?fsym={cur_from_code}&tsyms={cur_to_code}'
        rqst = requests.get(uri)
        try:
            rate = json.loads(rqst.content)[cur_to_code]
        except KeyError:
            raise ConversionException(f'Ошибка api при конвертации валют из {cur_from} в {cur_to}')
        total_amount = round(amount * rate, 3)
        text = f'Стоимость {amount} {cur_from} составляет <b>{total_amount}</b> в валюте {cur_to}'
        text += f"\n{amount} {cur_from_code} = {total_amount} {cur_to_code}"
        return text
