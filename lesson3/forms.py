from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[DataRequired()])
    surname = StringField('Фамилия: ', validators=[DataRequired()])
    email = EmailField('EMail: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    repeat_password = PasswordField('Повтор пароля: ', validators=[DataRequired()])