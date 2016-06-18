from flask_wtf import Form
from wtforms import BooleanField, DateField, PasswordField, StringField,\
    SubmitField, TextAreaField
from wtforms.validators import DataRequired


class SignUpForm(Form):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(Form):
    login = StringField("Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField("Login")


class PostForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class TagForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
