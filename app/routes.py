from . import forms
from . import models
from .app import app, db, lm
from config import POSTS_PER_PAGE
from flask import g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy_searchable import search

import datetime


@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))


@app.before_request
def before_request():
    g.search_form = forms.SearchForm()


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    posts = models.Post.query.order_by(
        models.Post.datetime.desc()
    ).paginate(page, POSTS_PER_PAGE, False)

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


@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        post = models.Post(
            form.title.data, form.content.data, datetime.datetime.utcnow(),
            current_user.id
        )
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add_post.html', form=form)


@app.route('/post/<id>')
def post(id):
    post = models.Post.query.get(id)
    return render_template('show_post.html', post=post)


@app.route('/search-posts/<query>')
@app.route('/search-posts/<query>/<int:page>')
def search_results(query, page=1):
    posts = models.Post.query.order_by(
        models.Post.datetime.desc()
    )
    posts = search(posts, query).paginate(page, POSTS_PER_PAGE, False)

    return render_template('search_posts.html', query=query, posts=posts)


@app.route('/search', methods=['POST'])
def search_posts():
    form = forms.PostForm()
    if g.search_form.validate_on_submit():
        return redirect(
            url_for('search_results', query=g.search_form.search.data)
        )
    return redirect(url_for('index'))
