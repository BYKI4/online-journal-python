import datetime
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime

from data import db_session
import datetime
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    about = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    classrooms = orm.relationship('Classroom', secondary='link')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Classroom(SqlAlchemyBase):
    __tablename__ = 'classroom'

    id = Column(Integer,primary_key=True, autoincrement=True)
    code = Column(String, nullable=True)
    marks = Column(String, default='')
    created_date = Column(DateTime, default=datetime.datetime.now)
    users = orm.relationship('User', secondary='link')


class Link(SqlAlchemyBase):
    __tablename__ = 'link'

    classroom_id = Column(Integer, ForeignKey('classroom.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
