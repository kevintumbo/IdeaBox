from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from flask_pagedown.fields import PageDownField

from models import User

# check if username exists
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists')

# check if email exists
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists')

# Register form validation
class RegisterForm(Form):
    first_name = StringField(
        'First name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]+$',
                message=("First name Should be letters only")
            ),
        ]
    )

    last_name = StringField(
        'Last name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]+$',
                message=('Last name Should be letters only')
            ),
        ]
    )

    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=('Username Should be one word, letters only')
            ),
            name_exists
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo('confirm_password', message='Passwords must match')
        ]
    )

    confirm_password = PasswordField(
        'Confirm_password',
        validators=[DataRequired()]
    )


# login form validation
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


# Post idea form
class IdeaForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    description = PageDownField('Description', validators=[DataRequired()])


# Post comment form
class CommentForm(Form):
    comment = TextAreaField('comment', validators=[DataRequired()])





