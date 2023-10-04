from flask import Blueprint, request
from api.add_route import tax_check

update = Blueprint('update', __name__)


# Обновление данных в коллекции
@update.route('/v1/update/tax', methods=['POST'])
def tax_update():
    region = request.json['region']
    tax = request.json['tax']
    if tax_check[region] is None:
        error_body = {'reason': 'такого налога не существует'}
        return error_body, 400
    else:
        tax_check[region] = tax
        return tax_check, 200