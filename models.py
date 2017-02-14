import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('ideas.db')

class User(UserMixin, Model):
    first_name = CharField(unique=True)
    last_name = CharField(unique=True)
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by =('-joined_at')

    @classmethod
    def create_user(cls, first_name, last_name, username,email, password):
        try:
            cls.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password =generate_password_hash(password)
            )
        except: IntegrityError:
            raise ValueError("User already exists")

    def initialize():
        DATABASE.connect()
        DATABASE.create_table([User], safe=True)
        DATABASE.close()