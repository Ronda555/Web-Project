from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    name = StringField(
        'Имя пользователя',
        validators=[DataRequired(), Length(min=3, max=32)]
    )

    password = PasswordField(
        'Пароль',
        validators=[DataRequired(), Length(min=4)]
    )

    submit = SubmitField('Зарегистрироваться')