from flask import Blueprint
from api.add_route import tax_check

fetch = Blueprint('fetch', __name__)

#Удаление символов
symbols_to_remove = "<>"


# Вывод списка налоговых ставок
@fetch.route('/v1/fetch/taxes', methods=['GET'])
def fetch_all():
    if tax_check is None:
        error_body = {'reason': 'Список пуст'}
        return error_body, 400
    else:
        return tax_check, 200


# Вывод данных по указанному коду региона
@fetch.route('/v1/fetch/tax/<id>', methods=['GET'])
def fetch_one(id):
    if tax_check is None:
        error_body = {'reason': 'Список пуст'}
        return error_body, 400
    else:
        if tax_check[id]:
            message = {id: tax_check[id]}
            return message, 200
        else:
            error_body = {'reason': 'Список пуст'}
            return error_body, 400


# Подсчёт налога (получение-подсчёт)
@fetch.route('/v1/fetch/calc/<id>/<price>/<month>', methods=['GET'])
def calc(id, price, month):
    if id is None or price is None or month is None:
        error_body = {'reason': 'Не корректные данные'}
        return error_body, 400
    if tax_check is None:
        error_body = {'reason': 'Список пуст'}
        return error_body, 400
    else:

        for symbol in symbols_to_remove:
            id = id.replace(symbol, "")
            price = price.replace(symbol, "")
            month = month.replace(symbol, "")

        if tax_check[id]:
            res = (int(price) * int(tax_check[id]) * int(month)) / 12
            message = {"res": res}
            return message, 200
        else:
            error_body = {'reason': 'Список пуст'}
            return error_body, 400