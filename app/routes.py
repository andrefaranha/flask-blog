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
    g.post_form = forms.PostForm()
    g.tags = models.Tag.query.all()


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


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    posts = models.Post.query.order_by(
        models.Post.datetime.desc()
    ).paginate(page, POSTS_PER_PAGE, False)

    return render_template('index.html', posts=posts)


@app.route("/tag/<id>")
@app.route("/tag/<id>/<int:page>")
def search_by_tag(id, page=1):
    posts = models.Post.query.filter(
        models.Tag.id.in_([id])
    ).order_by(
        models.Post.datetime.desc()
    ).paginate(page, POSTS_PER_PAGE, False)

    return render_template('list_posts_by_tag.html', id=id, posts=posts)


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
    if g.search_form.validate_on_submit():
        return redirect(
            url_for('search_results', query=g.search_form.search.data)
        )
    return redirect(url_for('index'))


@app.route('/write_post', methods=['POST'])
@login_required
def write_post():
    if g.post_form.validate_on_submit():
        post = models.Post(
            g.post_form.title.data, g.post_form.content.data,
            datetime.datetime.utcnow(), current_user.id
        )
        db.session.add(post)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = models.Post.query.get(id)
    form = forms.PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('edit_post.html', form=form)


@app.route('/delete_post/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = models.Post.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/post/<id>')
def post(id):
    post = models.Post.query.get(id)
    return render_template('show_post.html', post=post)


@app.route('/create_tag', methods=['POST'])
@login_required
def create_tag():
    form = forms.TagForm()
    if form.validate_on_submit():
        tag = models.Tag(form.name.data)
        db.session.add(tag)
        db.session.commit()

    return redirect(url_for('manage_tags'))


@app.route('/edit_tag/<id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    tag = models.Tag.query.get(id)
    form = forms.TagForm(obj=tag)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()

        return redirect(url_for('manage_tags'))
    return render_template('tag_form.html', form=form)


@app.route('/delete_tag/<id>')
@login_required
def delete_tag(id):
    tag = models.Tag.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('manage_tags'))


@app.route('/manage_tags')
@login_required
def manage_tags():
    form = forms.TagForm()

    return render_template('manage_tags.html', form=form)


@app.route('/add_tag/<tag_id>/to_post/<post_id>', methods=['GET', 'POST'])
@login_required
def add_tag_to_post(tag_id, post_id):
    tag = models.Tag.query.get(tag_id)
    post = models.Post.query.get(post_id)
    if tag not in post.tags:
        post.tags.append(tag)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/remove_tag/<tag_id>/from_post/<post_id>', methods=['GET', 'POST'])
@login_required
def remove_tag_from_post(tag_id, post_id):
    tag = models.Tag.query.get(tag_id)
    post = models.Post.query.get(post_id)
    if tag in post.tags:
        post.tags.remove(tag)
    db.session.commit()

    return redirect(url_for('index'))
