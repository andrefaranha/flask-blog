import app
import models
import routes

# from . import forms
# from flask import Flask, redirect, render_template, request, url_for
# # from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from . import app
#
# # import models
#
#
# # app = Flask(__name__)
# # app.config.from_object('config')
# # db = SQLAlchemy(app)
#
# from . import models

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'


# @app.route("/")
# def index():
#     return render_template('index.html')
#
#
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = forms.SignUpForm()
#     if form.validate_on_submit():
#         user = models.User(form.login.data, form.password.data)
#         db.session.add(user)
#         db.session.commit()
#
#         # login_user(user)
#         return redirect(request.args.get('next') or url_for('index'))
#     return render_template('signup.html', form=form)
#
#
# @app.route("/profile")
# def profile():
#     return render_template('index.html')

# @app.route("/about")
# def about():
#     return render_template('about.html')
#
#
# @app.route('/showSignUp')
# def showSignUp():
#     return render_template('signup.html')
#
#
# @app.route('/signUp', methods=['POST'])
# def signUp():
#     name = request.form['inputName']
#     email = request.form['inputEmail']
#     password = request.form['inputPassword']
#
#     if name and email and password:
#         user = models.User(email, password, name)
#         db.session.add(user)
#         db.session.commit()
#
#     return json.dumps({'html': '<span>Enter the required fields</span>'})
