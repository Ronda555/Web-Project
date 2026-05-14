from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    name = StringField(
        'Имя пользователя',
        validators=[DataRequired()]
    )

    submit = SubmitField('Поиск')