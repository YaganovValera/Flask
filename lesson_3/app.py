from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
app.secret_key = '1ceb13223c9c0de7a7db9157745965d095f81394e0d7cf7e341b59a33beff1a0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
csrf = CSRFProtect(app)
db.init_app(app)


# Creating a database
@app.cli.command("init-db")
def int_db():
    db.create_all()


# The main page
@app.route('/')
def home():
    status = session.get('logged_in') or False
    return render_template('base.html', status=status)


# Log out of account
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# Creating an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)
