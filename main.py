from flask import Flask, render_template, redirect, render_template, request
from data import db_session
from data.users import User
from forms.user import RegisterForm
from forms.Login import LoginForm
from forms.Search import SearchForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from data.messages import Message
import sqlalchemy as sql


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

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
        login_user(user)

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

        login_user(user)

        return redirect('/')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/')
    return 'Секретная страница'

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    form = SearchForm()

    users = []

    if form.validate_on_submit():

        session = db_session.create_session()

        users = session.query(User).filter(
            User.name.like(f"%{form.name.data}%")
        ).all()

    return render_template(
        'search.html',
        form=form,
        users=users
    )

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)

@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):

    session = db_session.create_session()

    receiver = session.query(User).get(user_id)

    if not receiver:
        return "Пользователь не найден"

    if request.method == 'POST':

        text = request.form.get('text')

        if text:

            message = Message()
            message.sender_id = current_user.id
            message.receiver_id = receiver.id
            message.text = text

            session.add(message)
            session.commit()

    messages = session.query(Message).filter(
        ((Message.sender_id == current_user.id) &
         (Message.receiver_id == receiver.id)) |
        ((Message.sender_id == receiver.id) &
         (Message.receiver_id == current_user.id))
    ).order_by(Message.created_date).all()

    return render_template(
        'chat.html',
        receiver=receiver,
        messages=messages
    )


@app.route('/dialogs')
@login_required
def dialogs():

    session = db_session.create_session()

    messages = session.query(Message).filter(
        sql.or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).all()
    print('11')

    user_ids = set()

    for msg in messages:

        if msg.sender_id != current_user.id:
            user_ids.add(msg.sender_id)

        if msg.receiver_id != current_user.id:
            user_ids.add(msg.receiver_id)

    users = []
    print('111')

    for user_id in user_ids:

        user = session.query(User).get(user_id)

        if user:
            users.append(user)

    return render_template(
        'dialogs.html',
        users=users
    )

def main():
    # создание базы данных
    db_session.global_init("database.db")
    app.run()

if __name__ == '__main__':
    main()