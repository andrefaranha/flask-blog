import datetime
import os
import unittest

from app.app import app
from app.app import db
from app import models
from flask import url_for


POSTGRESQL_TEST_DB = "postgresql://postgres:admin@localhost/flask_blog_test"


class TestCase(unittest.TestCase):
    ROOT_PAGE = 'http://localhost/'
    USER_1_LOGIN = 'user_1'
    USER_1_PASSWD = '1'
    USER_1_NAME = 'User 1'

    USER_2_LOGIN = 'user_2'
    USER_2_PASSWD = '2'
    USER_2_NAME = 'User 2'

    USER_3_LOGIN = 'user_3'
    USER_3_PASSWD = '3'
    USER_3_NAME = 'User 3'

    def _populate_db_with_users(self):
        users = [
            models.User(
                self.USER_1_LOGIN, self.USER_1_PASSWD, self.USER_1_NAME
            ),
            models.User(
                self.USER_2_LOGIN, self.USER_2_PASSWD, self.USER_2_NAME
            ),
            models.User(
                self.USER_3_LOGIN, self.USER_3_PASSWD, self.USER_3_NAME
            ),
        ]

        for user in users:
            db.session.add(user)
        db.session.commit()

    def _create_post(self, title='Default', user_login=None, tag=None):
        if user_login is None:
            user_login = self.USER_1_LOGIN

        user = models.User.query.filter(
            models.User.login == user_login
        ).first()

        post = models.Post(
            title, 'Post Content',
            datetime.datetime.strptime("20091229050936", "%Y%m%d%H%M%S"),
            user.id
        )

        db.session.add(post)

        if tag:
            post.tags.append(tag)
        db.session.commit()

        return models.Post.query.filter(models.Post.title == title).first()

    def _create_tag(self, name='Default'):
        tag = models.Tag(name)
        db.session.add(tag)
        db.session.commit()

        return models.Tag.query.filter(models.Tag.name == name).first()

    def _log_user(self, login, password):
        self.app.post('/login', data=dict(
            login=login,
            password=password
        ), follow_redirects=False)

    def _log_valid_user(self):
        self._log_user(self.USER_1_LOGIN, self.USER_1_PASSWD)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_TEST_DB
        self.app = app.test_client()
        db.drop_all()
        db.get_engine(app).connect().execute(
            'DROP FUNCTION IF EXISTS post_search_vector_update();'
        )
        db.create_all()
        self._populate_db_with_users()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_login(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_valid_post_login(self):
        result = self.app.post('/login', data=dict(
            login='user_1',
            password='1'
        ), follow_redirects=False)

        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_invalid_post_login(self):
        result = self.app.post('/login', data=dict(
            login='A',
            password='A'
        ), follow_redirects=False)

        self.assertEqual(result.status_code, 200)

    def test_get_logout(self):
        self.app.post('/login', data=dict(
            login='user_1',
            password='1'
        ), follow_redirects=False)
        result = self.app.get('/logout')

        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_index_with_paginate(self):
        result = self.app.get('/1')
        self.assertEqual(result.status_code, 200)

    def test_index_with_invalid_paginate(self):
        result = self.app.get('/0')
        self.assertEqual(result.status_code, 404)

    def test_index_with_paginate_page_bigger_than_pagination(self):
        self._create_post(self.USER_1_LOGIN)
        result = self.app.get('/999')
        self.assertEqual(result.status_code, 404)

    def test_search_by_tag(self):
        tag = self._create_tag()
        result = self.app.get('/tag/' + str(tag.id))
        self.assertEqual(result.status_code, 200)

    def test_search_by_invalid_tag(self):
        result = self.app.get('/tag/999')
        self.assertEqual(result.status_code, 200)

    def test_search_by_tag_with_invalid_pagination(self):
        tag = self._create_tag()
        self._create_post(tag=tag)
        result = self.app.get('/tag/' + str(tag.id) + '/0')
        self.assertEqual(result.status_code, 404)

    def test_search_by_tag_with_paginate_page_bigger_than_pagination(self):
        tag = self._create_tag()
        self._create_post(tag=tag)
        result = self.app.get('/tag/' + str(tag.id) + '/999')
        self.assertEqual(result.status_code, 404)

    def test_search_results(self):
        post = self._create_post()
        result = self.app.get('/search-posts/' + post.title)
        self.assertEqual(result.status_code, 200)

    def test_search_results_with_non_existing_query(self):
        post = self._create_post()
        result = self.app.get('/search-posts/NOT_AN_EXISTING_QUERY')
        self.assertEqual(result.status_code, 200)

    def test_search_results_with_invalid_pagination(self):
        result = self.app.get('/search-posts/NOT_AN_EXISTING_QUERY/0')
        self.assertEqual(result.status_code, 404)

    def test_search_results_with_paginate_page_bigger_than_pagination(self):
        post = self._create_post()
        result = self.app.get('/search-posts/' + post.title + '/999')
        self.assertEqual(result.status_code, 404)

    def test_post_search_posts(self):
        result = self.app.post('/search', data=dict(
            search='A'
        ), follow_redirects=False)

        self.assertEqual(result.location, self.ROOT_PAGE + 'search-posts/A')

    def test_invalid_post_search_posts(self):
        result = self.app.post('/search', data=dict(
            search=''
        ), follow_redirects=False)

        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_post_write_post(self):
        self._log_valid_user()
        result = self.app.post('/write_post', data=dict(
            title='Title',
            content='Content'
        ), follow_redirects=False)

        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_invalid_post_write_post(self):
        self._log_valid_user()
        result = self.app.post('/write_post', data=dict(
            title='',
            content='Content'
        ), follow_redirects=False)

        self.assertEqual(result.status_code, 200)

    def test_post_write_post_without_logged_user(self):
        result = self.app.post(
            '/write_post', data=dict(
                title='Title',
                content='Content'
            ), follow_redirects=False
        )

        self.assertEqual(
            result.location, self.ROOT_PAGE + 'login?next=%2Fwrite_post'
        )

    def test_edit_invalid_post(self):
        self._log_valid_user()
        result = self.app.get('/edit_post/999')
        self.assertEqual(result.status_code, 404)

    def test_edit_post(self):
        self._log_valid_user()
        post = self._create_post()
        result = self.app.get('/edit_post/' + str(post.id))
        self.assertEqual(result.status_code, 200)

    def test_edit_post_without_logged_user(self):
        post = self._create_post()
        result = self.app.get('/edit_post/' + str(post.id))
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fedit_post%2F' + str(post.id)
        )

    def test_post_edit_post_without_logged_user(self):
        post = self._create_post()
        result = self.app.post(
            '/edit_post/' + str(post.id), data=dict(
                title='Title',
                content='Content'
            )
        )
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fedit_post%2F' + str(post.id)
        )

    def test_post_edit_invalid_post(self):
        self._log_valid_user()
        result = self.app.post(
            '/edit_post/999', data=dict(
                title='Title',
                content='Content'
            )
        )
        self.assertEqual(result.status_code, 404)

    def test_post_edit_post(self):
        self._log_valid_user()
        post = self._create_post()
        result = self.app.post(
            '/edit_post/' + str(post.id), data=dict(
                title='New Title',
                content='New Content'
            )
        )
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_delete_post_without_logged_user(self):
        result = self.app.get('/delete_post/999')
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fdelete_post%2F999'
        )

    def test_delete_invalid_post(self):
        self._log_valid_user()
        result = self.app.get('/delete_post/999')
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_delete_post(self):
        self._log_valid_user()
        post = self._create_post()
        result = self.app.get('/delete_post/' + str(post.id))
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_show_post(self):
        post = self._create_post()
        result = self.app.get('/post/' + str(post.id))
        self.assertEqual(result.status_code, 200)

    def test_show_invalid_post(self):
        result = self.app.get('/post/999')
        self.assertEqual(result.status_code, 404)

    def test_post_create_tag(self):
        self._log_valid_user()
        result = self.app.post(
            '/create_tag', data=dict(name='Name'), follow_redirects=False
        )

        self.assertEqual(result.location, self.ROOT_PAGE + 'manage_tags')

    def test_invalid_post_create_tag(self):
        self._log_valid_user()
        result = self.app.post(
            '/create_tag', data=dict(name='',), follow_redirects=False
        )

        self.assertEqual(result.location, self.ROOT_PAGE + 'manage_tags')

    def test_post_create_tag_without_logged_user(self):
        result = self.app.post(
            '/create_tag', data=dict(name='',), follow_redirects=False
        )

        self.assertEqual(
            result.location, self.ROOT_PAGE + 'login?next=%2Fcreate_tag'
        )

    def test_edit_invalid_tag(self):
        self._log_valid_user()
        result = self.app.get('/edit_tag/999')
        self.assertEqual(result.status_code, 404)

    def test_edit_tag(self):
        self._log_valid_user()
        tag = self._create_tag()
        result = self.app.get('/edit_tag/' + str(tag.id))
        self.assertEqual(result.status_code, 200)

    def test_edit_tag_without_logged_user(self):
        tag = self._create_tag()
        result = self.app.get('/edit_tag/' + str(tag.id))
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fedit_tag%2F' + str(tag.id)
        )

    def test_post_edit_tag_without_logged_user(self):
        tag = self._create_tag()
        result = self.app.post(
            '/edit_tag/' + str(tag.id), data=dict(name='New Name')
        )
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fedit_tag%2F' + str(tag.id)
        )

    def test_post_edit_invalid_tag(self):
        self._log_valid_user()
        result = self.app.post('/edit_tag/999', data=dict(name='New Name'))
        self.assertEqual(result.status_code, 404)

    def test_post_edit_tag(self):
        self._log_valid_user()
        tag = self._create_tag()
        result = self.app.post(
            '/edit_tag/' + str(tag.id), data=dict(name='New Name')
        )
        self.assertEqual(result.location, self.ROOT_PAGE + 'manage_tags')

    def test_delete_tag_without_logged_user(self):
        result = self.app.get('/delete_tag/999')
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fdelete_tag%2F999'
        )

    def test_delete_invalid_tag(self):
        self._log_valid_user()
        result = self.app.get('/delete_tag/999')
        self.assertEqual(result.location, self.ROOT_PAGE + 'manage_tags')

    def test_delete_tag(self):
        self._log_valid_user()
        tag = self._create_tag()
        result = self.app.get('/delete_tag/' + str(tag.id))
        self.assertEqual(result.location, self.ROOT_PAGE + 'manage_tags')

    def test_get_manage_tags(self):
        self._log_valid_user()
        result = self.app.get('/manage_tags')
        self.assertEqual(result.status_code, 200)

    def test_get_manage_tags_without_logged_user(self):
        result = self.app.get('/manage_tags')
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fmanage_tags'
        )

    def test_post_manage_tags(self):
        self._log_valid_user()
        result = self.app.post(
            '/manage_tags', data=dict(name='Name'), follow_redirects=False
        )
        self.assertEqual(result.status_code, 200)

    def test_invalid_post_manage_tags(self):
        self._log_valid_user()
        result = self.app.post(
            '/manage_tags', data=dict(name=''), follow_redirects=False
        )
        self.assertEqual(result.status_code, 200)

    def test_post_manage_tag_without_logged_user(self):
        result = self.app.post(
            '/manage_tags', data=dict(name='',), follow_redirects=False
        )
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fmanage_tags'
        )

    def test_get_add_tag_to_post_without_logged_user(self):
        result = self.app.get('/add_tag/999/to_post/999')
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fadd_tag%2F999%2Fto_post%2F999'
        )

    def test_get_add_invalid_tag_to_invalid_post(self):
        self._log_valid_user()
        result = self.app.get('/add_tag/999/to_post/999')
        self.assertEqual(result.status_code, 404)

    def test_get_add_tag_to_invalid_post(self):
        self._log_valid_user()
        tag = self._create_tag()
        result = self.app.get('/add_tag/' + str(tag.id) + '/to_post/999')
        self.assertEqual(result.status_code, 404)

    def test_get_add_invalid_tag_to_post(self):
        self._log_valid_user()
        post = self._create_post()
        result = self.app.get('/add_tag/999/to_post/' + str(post.id))
        self.assertEqual(result.status_code, 404)

    def test_get_add_tag_to_post(self):
        self._log_valid_user()
        tag = self._create_tag()
        post = self._create_post()
        result = self.app.get(
            '/add_tag/' + str(tag.id) + '/to_post/' + str(post.id)
        )
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_get_add_tag_to_post_associated(self):
        self._log_valid_user()
        tag = self._create_tag()
        post = self._create_post(tag=tag)
        result = self.app.get(
            '/add_tag/' + str(tag.id) + '/to_post/' + str(post.id)
        )
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_get_remove_tag_from_post_without_logged_user(self):
        result = self.app.get('/remove_tag/999/from_post/999')
        self.assertEqual(
            result.location,
            self.ROOT_PAGE + 'login?next=%2Fremove_tag%2F999%2Ffrom_post%2F999'
        )

    def test_get_remove_invalid_tag_from_invalid_post(self):
        self._log_valid_user()
        result = self.app.get('/remove_tag/999/from_post/999')
        self.assertEqual(result.status_code, 404)

    def test_get_remove_tag_from_invalid_post(self):
        self._log_valid_user()
        tag = self._create_tag()
        result = self.app.get('/remove_tag/' + str(tag.id) + '/from_post/999')
        self.assertEqual(result.status_code, 404)

    def test_get_remove_invalid_tag_from_post(self):
        self._log_valid_user()
        post = self._create_post()
        result = self.app.get('/remove_tag/999/from_post/' + str(post.id))
        self.assertEqual(result.status_code, 404)

    def test_get_remove_tag_from_post(self):
        self._log_valid_user()
        tag = self._create_tag()
        post = self._create_post()
        result = self.app.get(
            '/remove_tag/' + str(tag.id) + '/from_post/' + str(post.id)
        )
        self.assertEqual(result.location, self.ROOT_PAGE)

    def test_get_remove_tag_from_post_associated(self):
        self._log_valid_user()
        tag = self._create_tag()
        post = self._create_post(tag=tag)
        result = self.app.get(
            '/remove_tag/' + str(tag.id) + '/from_post/' + str(post.id)
        )
        self.assertEqual(result.location, self.ROOT_PAGE)


if __name__ == '__main__':
    unittest.main()
