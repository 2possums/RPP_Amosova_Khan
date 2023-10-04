from flask import Blueprint, request

add = Blueprint('add', __name__)

tax_check = {}


# enpoint добавления значения в список
@add.route('/v1/add/tax', methods=['POST'])
def add_new():
    region = request.json['region']
    tax = request.json['tax']
    if region in tax_check:
        error_body = {'reason': 'такой налог уже существует'}
        return error_body, 400
    else:
        tax_check[region] = tax
        return tax_check, 200
