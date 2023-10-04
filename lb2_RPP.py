from flask import Flask
from api.fetch_route import fetch
from api.update_route import update
from api.add_route import add


app = Flask(__name__)

#Связь между файлами
app.register_blueprint(add)
app.register_blueprint(fetch)
app.register_blueprint(update)

#Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)