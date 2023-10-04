from flask import Flask, request
import psycopg2 as pg

app = Flask(__name__)

# подключение к бд
conn = pg.connect(user='postgres', password='зщыепкуы', host='localhost', port='5433', database='lb1_RPP')
cursor = conn.cursor()


# проверка данных с объектах налогооблажения
def check(id, name):
    cursor.execute("""Select id from region""")
    region = cursor.fetchall()
    if id in region:
        return ('400 BAD REQUEST')
    else:
        cursor.execute("""insert into region (id, name)
                                                 values (%(id)s, %(name)s);""",
                       {"id": id, "name": name})
        conn.commit()
        return ('200')


# проверка региона
def check_tax_param(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate):
    cursor.execute("""Select id from tax_param""")
    region = cursor.fetchall()
    if id in region:
        return ('400 BAD REQUEST')
    else:
        add_tax_param_bd(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
        return ('200')


# Добавление данных с объектом налогооблажения
def add_tax_param_bd(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate):
    cursor.execute("""insert into tax_param (
                                        id,
                                        city_id, 
                                        from_hp_car, 
                                        to_hp_car, 
                                        from_production_year_car, 
                                        to_production_year_car, 
                                        rate)
                                         values (
                                         %(id)s, 
                                         %(city_id)s, 
                                         %(from_hp_car)s, 
                                         %(to_hp_car)s, 
                                         %(from_production_year_car)s, 
                                         %(to_production_year_car)s, 
                                         %(rate)s);""",
                   {
                       "id": id,
                       "city_id": city_id,
                       "from_hp_car": from_hp_car,
                       "to_hp_car": to_hp_car,
                       "from_production_year_car": from_production_year_car,
                       "to_production_year_car": to_production_year_car,
                       "rate": rate})
    conn.commit()


# Добавление данных с объектом налогооблажения
def add_auto_bd(id, city_id, tax_id, name, horse_power, production_year, tax):
    try:
        cursor.execute("""insert into auto (
                                            id,
                                            city_id, 
                                            tax_id, 
                                            name, 
                                            horse_power, 
                                            production_year, 
                                            tax)
                                             values (
                                             %(id)s,
                                             %(city_id)s, 
                                             %(tax_id)s, 
                                             %(name)s, 
                                             %(horse_power)s, 
                                             %(production_year)s, 
                                             %(tax)s);""",
                       {
                           "id": id,
                           "city_id": city_id,
                           "tax_id": tax_id,
                           "name": name,
                           "horse_power": horse_power,
                           "production_year": production_year,
                           "tax": tax})
    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
        return 400

    conn.commit()
    return 200


# Задание 1 endpoint POST добавления информации о регионе
@app.route('/v1/add/region', methods=['POST'])
def add_region():
    if 'id' not in request.json or 'city_name' not in request.json:
        error_body = {'reason': 'id и/или name пуст(ы)'}
        return error_body, 400

    id = request.json['id']
    name = request.json['city_name']
    response = check(id, name)
    return response


# Задание 2 endpoint добавления объекта налогообложения POST
@app.route('/v1/add/tax-param', methods=['POST'])
def add_tax_param():
    if 'id' not in request.json or 'city_id' not in request.json or 'from_hp_car' not in request.json or 'to_hp_car' not in request.json or 'from_production_year_car' not in request.json or 'to_production_year_car' not in request.json or 'rate' not in request.json:
        error_body = {'reason': 'Одно/несколько поле(й) пуст(ы)'}
        return error_body, 400

    city_id = request.json['city_id']

    cursor.execute("""Select * from region where id = %(id)s""", {'id': city_id})
    region = cursor.fetchone()

    if region is None:
        return '400 BAD REQUEST'

    # выгрузка данных из json (postman)
    id = request.json['id']
    city_id = request.json['city_id']
    from_hp_car = request.json['from_hp_car']
    to_hp_car = request.json['to_hp_car']
    from_production_year_car = request.json['from_production_year_car']
    to_production_year_car = request.json['to_production_year_car']
    rate = request.json['rate']

    response = check_tax_param(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car,
                               rate)
    return response


# Задание 3
@app.route('/v1/add/auto', methods=['POST'])
def add_auto():
    if 'id' not in request.json or 'city_id' not in request.json or 'tax_id' not in request.json or 'name' not in request.json or 'horse_power' not in request.json or 'production_year' not in request.json:
        error_body = {'reason': 'Одно/несколько поле(й) пуст(ы)'}
        return error_body, 400

    city_id = request.json['city_id']

    cursor.execute("Select * from region where id = %(id)s", {'id': city_id})
    region = cursor.fetchone()

    tax_id = request.json['tax_id']
    horse_power = request.json['horse_power']
    production_year = request.json['production_year']

    cursor.execute("""Select rate from tax_param where id = %(id)s
                        and %(horse_power)s <= to_hp_car 
                        and %(horse_power)s > from_hp_car
                        and  %(production_year)s <= to_production_year_car
                        and  %(production_year)s > from_production_year_car
                        """, {'id': tax_id, 'horse_power': horse_power, 'production_year': production_year})
    #Выгрузка данных из БД в переменную
    rate = cursor.fetchone()

    if region is None or rate is None:
        return '400 BAD REQUEST'

    id = request.json['id']
    name = request.json['name']

    tax = rate[0] * horse_power

#Добавление данных в БД
    response = add_auto_bd(id, city_id, tax_id, name, horse_power, production_year, tax)
    return "Auto added", response


# Задание 4 endpoint получения информации по автомобилю
@app.route('/v1/auto/<id>', methods=['GET'])
def auto(id):
    cursor.execute("SELECT * FROM auto WHERE id=%(id)s", {'id': int(id)})
    auto = cursor.fetchone()
    print(auto)
    if auto is None:
        return '400 BAD REQUEST'
    else:
        message = {"Auto": f"{auto[6]}"}
        return message


if __name__ == '__main__':
    app.run(debug=True)
