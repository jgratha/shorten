import unittest
from datetime import timezone, datetime

import app
from app.main.models import Shortcode, Url, Redirect
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

    def test_stats_successful(self):

        dt_shortcode = datetime(2021, 1, 1, tzinfo=timezone.utc)
        dt_r1 = datetime(2021, 1, 2, tzinfo=timezone.utc)
        dt_r2 = datetime(2021, 1, 3, 0, 0, 1, 123000, tzinfo=timezone.utc)

        url = Url(url='https://www.test.nl')
        shortcode = Shortcode(
            shortcode='abc123',
            url=url,
            created_at=dt_shortcode
        )
        r1 = Redirect(shortcode=shortcode, created_at=dt_r1)
        r2 = Redirect(shortcode=shortcode, created_at=dt_r2)
        app.db.session.add(r1)
        app.db.session.add(r2)

        response = self.client.get('/abc123/stats')

        assert response.status_code == 200
        assert response.json['created'] == '2021-0101T00:00:00.000Z'
        assert response.json['lastRedirect'] == '2021-0103T00:00:01.123Z'
        assert response.json['redirectCount'] == 2

    def test_no_stats_successful(self):
        dt_shortcode = datetime(2021, 1, 1, tzinfo=timezone.utc)
        dt_r1 = datetime(2021, 1, 2, tzinfo=timezone.utc)
        dt_r2 = datetime(2021, 1, 3, 0, 0, 1, 123000, tzinfo=timezone.utc)

        url = Url(url='https://www.test.nl')
        shortcode = Shortcode(
            shortcode='abc123',
            url=url,
            created_at=dt_shortcode
        )
        app.db.session.add(shortcode)

        response = self.client.get('/abc123/stats')

        assert response.status_code == 200
        assert response.json['created'] == '2021-0101T00:00:00.000Z'
        assert response.json['lastRedirect'] == None
        assert response.json['redirectCount'] == 0

    def test_shortcode_not_found(self):
        response = self.client.get('/abc123/stats')

        assert response.status_code == 404
        assert response.json['message'] == 'Shortcode not found'
