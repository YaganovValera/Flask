from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/clothing')
def clothing():
    products = [
        {'id': 1, 'name': 'Футболка', 'price': 999.99, 'description': 'Удобная хлопчатобумажная футболка',
         'image': 'img/t-shirt.png'},
        {'id': 2, 'name': 'Джинсы', 'price': 1999.99, 'description': 'Классические синие джинсы',
         'image': 'img/jeans.png'},
    ]
    return render_template('category.html', category='Одежда', products=products)


@app.route('/shoes')
def shoes():
    products = [
        {'id': 3, 'name': 'Кроссовки', 'price': 1499.99, 'description': 'Стильные спортивные кроссовки',
         'image': 'img/cros.png'},
        {'id': 4, 'name': 'Ботинки', 'price': 69.99, 'description': 'Прочные кожаные ботинки',
         'image': 'img/bot.png'},
    ]
    return render_template('category.html', category='Обувь', products=products)


if __name__ == '__main__':
    app.run(debug=True)