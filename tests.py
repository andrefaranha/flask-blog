import os
import unittest

from app.app import app, db
from app import models


POSTGRESQL_TEST_DB = "postgresql://postgres:admin@localhost/flask_blog_test"


class TestCase(unittest.TestCase):
    def _populate_db_with_users(self):
        users = [
            models.User('user_1', '1'),
            models.User('user_2', '2'),
        ]

        for user in users:
            db.session.add(user)
        db.session.commit()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_TEST_DB
        self.app = app.test_client()
        db.create_all()
        self._populate_db_with_users()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_valid_login(self):
        rv = self.app.post('/login', data=dict(
            login='user_1',
            password='1'
        ), follow_redirects=True)

        print rv.data


if __name__ == '__main__':
    unittest.main()
