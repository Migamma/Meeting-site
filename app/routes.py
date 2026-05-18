from flask import render_template
import sqlalchemy as sa
from flask_bootstrap import Bootstrap
from flask import render_template, flash, redirect, url_for
from app import app,db
from app.forms import LoginForm, EventForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from app.models import User,Event
import datetime

bootstrap=Bootstrap(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user=db.session.scalar(sa.select(User).where(User.username == form.username.data))
    # flash('Login requested for user {}, remember_me={}'.format(
    #   form.username.data, form.remember_me.data))
    if user is None or not user.check_password(form.password.data):
      flash('Не правильный логин или пароль')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('events', username=current_user.username))
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/events/<username>')
@login_required
def events(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # events = [
        # {'owner': user, 'message': 'Event 1', 'duration':2, "timeschedule": datetime.datetime.now()  },
        # {'owner': user, 'message': 'Event 2', 'duration': 1, "timeschedule": datetime.datetime.now() }
    # ]
    query=current_user.events.select()

    events=db.session.scalars(query).all()
    return render_template('events.html', user=user, events=events)

@app.route('/events/newevent',methods=['GET', 'POST'])
@login_required
def newevent():
   form=EventForm()
   if form.validate_on_submit():

      e=Event(message=form.message.data, duration=form.duration.data,timeSchedule=form.scheduletime.data,username=current_user.id)
      db.session.add(e)
      db.session.commit()
      return redirect(url_for('events', username=current_user.username))
   return render_template('newevent.html',form=form)
      
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляю, вы создали нового пользователя')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

@app.route('/events/<id>',methods=['POST'])
@login_required
def deletevent(id):
   event_del = db.first_or_404(sa.select(Event).where(Event.id == int(id)))
   db.session.delete(event_del)
   db.session.commit()
   flash("Запись успешно удалена")
   return redirect(url_for('events', username=current_user.username))