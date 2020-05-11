from flask import Flask
from flask import url_for, request
from flask import render_template
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import redirect
from wtforms.fields.html5 import EmailField
from flask_sqlalchemy import SQLAlchemy
#  from data.__all_models import User, Classroom, Link
from data.__all_models import User, Classroom, Link


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['username'] = "Учащийся"
    param['title'] = 'Домашняя страница'
    return render_template("index.html", **param)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/marks")
        return render_template('login.html',
                               Mark="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

def main():
    app.run()

from data import db_session
db_session.global_init("db/blogs.sqlite")


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя и Фамилия', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            form.password_again.errors.append("Пароли не совпадают")
            return render_template('register.html', title='Регистрация', form=form)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            form.email.errors.append("Такой пользователь уже есть")
            return render_template('register.html', title='Регистрация', form=form)
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/messages')
def messages():
    return "Здесь пока ничего нет..."

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/marks')
def marks():
    return render_template('marks.html')

@app.route('/change_password')
def change_password():
    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
