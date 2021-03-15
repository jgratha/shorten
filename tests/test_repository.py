import unittest
from datetime import datetime

import app
from app.main.models import Url, Shortcode, Redirect
from app.main import repository
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class RepositoryTest(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.db.create_all()

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()
        self.app_context.pop()

    def test_does_shortcode_exist(self):
        session = app.db.session

        url = Url(url='https://www.test.nl')
        shortcode = Shortcode(shortcode='abc123', url=url)
        session.add(shortcode)

        assert repository.does_shortcode_exist('abc123')
        assert repository.does_shortcode_exist('xyz456') is False

    def test_insert_shortcode(self):
        repository.insert_shortcode('abc123', 'www.test.nl')
        shortcode = Shortcode.query.filter_by(shortcode='abc123').first()
        assert shortcode.url.url == 'www.test.nl'

    def test_register_redirect(self):
        repository.insert_shortcode('abc123', 'www.test.nl')
        shortcode_model = repository.get_shortcode('abc123')
        repository.register_redirect(shortcode_model)
        repository.register_redirect(shortcode_model)

        session = app.db.session

        result = (
            session.query(Redirect)
                .join(Shortcode)
                .filter(Shortcode.shortcode == "abc123")
                .all()
        )

        assert len(result) == 2

    def test_get_shortcode_stats(self):
        session = app.db.session

        shortcode = Shortcode(shortcode='abc123',
                              created_at=datetime(2021, 1, 1))
        r1 = Redirect(created_at=datetime(2021, 1, 1), shortcode=shortcode)
        r2 = Redirect(created_at=datetime(2021, 1, 2), shortcode=shortcode)

        session.add(r1)
        session.add(r2)

        stats = repository.get_shortcode_stats(shortcode)

        assert stats.created == shortcode.created_at
        assert stats.lastRedirect == r2.created_at
        assert stats.redirectCount == 2
