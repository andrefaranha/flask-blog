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
    # datetime = DateField("Date", validators=[DataRequired()])
    # user_id = IntegerField("User Id", validators=[DataRequired()])
    submit = SubmitField("Write Post")


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
