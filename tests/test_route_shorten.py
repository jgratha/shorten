import json
import unittest
import app
from app.main.models import Shortcode
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

    def test_insert_shortcode_success(self):
        data = dict(
            url='https://www.test.com',
            shortcode='abc123'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )
        assert response.status_code == 201
        assert response.json['shortcode'] == 'abc123'

    def test_insert_shortcode_without_shortcode_success(self):
        data = dict(
            url='https://www.test.com'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )

        assert response.status_code == 201
        assert len(response.json['shortcode']) == 6

    def test_insert_invalid_shortcode(self):
        data = dict(
            url='https://www.test.com',
            shortcode='abc'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )
        assert response.status_code == 412
        assert response.json['message'] == 'The provided shortcode is invalid'


    def test_insert_taken_shortcode(self):

        shortcode = Shortcode(shortcode='abc123')
        app.db.session.add(shortcode)

        data = dict(
            url='https://www.test.com',
            shortcode='abc123'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )
        assert response.status_code == 409
        assert response.json['message'] == 'Shortcode already in use'

    def test_insert_shortcode_invalid_url(self):
        data = dict(
            url='www.test.com', # no http(s)
            shortcode='abc123'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )
        assert response.status_code == 412
        assert response.json['message'] == 'The provided url is invalid'

    def test_insert_shortcode_missing_url(self):
        data = dict(
            shortcode='abc123'
        )
        response = self.client.post(
            '/shorten',
            data=json.dumps(data)
        )
        assert response.status_code == 400
        assert response.json['message'] == 'Url not present'
