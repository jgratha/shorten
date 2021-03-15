import unittest

import app
from app.main.models import Shortcode, Url
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class RouteShortenTest(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()
        self.app_context.pop()

    def test_successful(self):
        url = Url(url='https://www.test.nl')
        shortcode = Shortcode(shortcode='abc123', url=url)
        app.db.session.add(shortcode)

        response = self.client.get('/abc123')

        assert response.status_code == 302
        assert response.location == 'https://www.test.nl'

    def test_shortcode_not_found(self):
        response = self.client.get('/abc123')

        assert response.status_code == 404
        assert response.json['message'] == 'Shortcode not found'
