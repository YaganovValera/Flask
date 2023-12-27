from flask import Flask, render_template, session, request, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/')
def home():
    user_name = request.cookies.get('user_name')
    status = user_name is not None
    return render_template('base.html', status=status, user_name=user_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        response = make_response(redirect(url_for('home')))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)

        return response

    return render_template('form.html', title='Вход')


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')
    return response


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
