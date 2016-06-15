from . import forms
from . import models
from .app import app, db, lm
import datetime
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user


@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.route("/")
def index():
    posts = models.Post.query.order_by(models.Post.datetime.desc()).all()
    # from sqlalchemy_searchable import search
    # query = db.session.query(models.Post)
    # query = search(query, 'blog')
    # print query.all()

    return render_template('index.html', posts=posts)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        user = models.User(form.login.data, form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter(
            models.User.login == form.login.data
        ).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/addPost', methods=['GET', 'POST'])
@login_required
def addPost():
    form = forms.PostForm()
    if form.validate_on_submit():
        post = models.Post(
            form.title.data, form.content.data, datetime.datetime.utcnow(),
            current_user.id
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('addPost.html', form=form)


@app.route('/post/<id>')
def post(id):
    post = models.Post.query.get(id)
    return render_template('post.html', post=post)
