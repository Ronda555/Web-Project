from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.Login import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return 'в разработке'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        session = db_session.create_session()

        existing_user = session.query(User).filter(
            User.name == form.name.data
        ).first()

        if existing_user:
            return render_template(
                'register.html',
                form=form,
                message='Пользователь уже существует'
            )

        user = User()
        user.name = form.name.data
        user.about = 'Новый пользователь'

        user.set_password(form.password.data)

        session.add(user)
        session.commit()

        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        session = db_session.create_session()

        user = session.query(User).filter(
            User.name == form.name.data
        ).first()

        if not user:
            return render_template(
                'login.html',
                form=form,
                message='Пользователь не найден'
            )

        if not user.check_password(form.password.data):
            return render_template(
                'login.html',
                form=form,
                message='Неверный пароль'
            )

        return redirect('/')

    return render_template('login.html', form=form)

def main():
    # создание базы данных
    db_session.global_init("database.db")
    app.run()

if __name__ == '__main__':
    main()