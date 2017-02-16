import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
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
        order_by = ('-joined_at',)

    def get_ideas(self):
        return Idea.select().where(Idea.user == self)

    @classmethod
    def create_user(cls, first_name, last_name, username, email, password):
        try:
            cls.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Idea(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        related_name='ideas'
    )

    title = TextField()
    description = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Comment(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        related_name='comments'
    )
    idea = ForeignKeyField(
        rel_model=Idea,
        related_name='comments'
    )
    comment = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Idea, Comment], safe=True)
    DATABASE.close()
