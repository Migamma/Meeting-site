from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, BooleanField, SubmitField, PasswordField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from datetime import datetime

class LoginForm(FlaskForm):
  username = StringField('Имя:', validators=[DataRequired()])
  password = PasswordField('Пароль:', validators=[DataRequired()])
  remember_me = BooleanField('Запомнить меня')
  submit = SubmitField('Зайти')

class EventForm(FlaskForm):
  message = StringField('Мероприятие:', validators=[DataRequired()])
  scheduletime = DateTimeLocalField('Когда:', format='%Y-%m-%dT%H:%M',  validators=[DataRequired()],default=datetime.now())
  duration = IntegerField('Продолжительность, в часах:', validators=[DataRequired()])
  submit = SubmitField('Добавить')

class RegistrationForm(FlaskForm):
  username = StringField('Имя:', validators=[DataRequired()])
  password = PasswordField('Пароль:', validators=[DataRequired()])
  password2 = PasswordField('Повторите пароль:', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Регистрация')