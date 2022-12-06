# Forms for the TickTock website

import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = wtforms.StringField("Search")


class PostForm(FlaskForm):
    content = wtforms.TextAreaField("Content", validators=[DataRequired()])


class AuthForm(FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    password = wtforms.PasswordField("Password", validators=[DataRequired()])


class LogoutForm(FlaskForm):
    ...
