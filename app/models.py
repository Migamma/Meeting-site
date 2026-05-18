from typing import Optional
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db,login

@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))

class User(UserMixin,db.Model):
  __tablename__="user_table"
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
  password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
  events: so.WriteOnlyMapped['Event'] = so.relationship(back_populates='owner')
  
  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Event(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  message: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=False)
  timeSchedule: so.Mapped[datetime] = so.mapped_column(sa.DateTime, index=True, unique=False)
  duration: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, unique=False)
  username: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user_table.id"))
  owner: so.Mapped[User] = so.relationship(back_populates='events')
  
  def __repr__(self):
    return '<User {}>'.format(self.message)