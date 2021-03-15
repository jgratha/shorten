import unittest

from app.main import helpers

class HelpersTest(unittest.TestCase):

    def test_is_valid_shortcode(self):
        assert helpers.is_valid_shortcode('Abc12_')
        assert helpers.is_valid_shortcode('abcde.') is False # invalid '.'
        assert helpers.is_valid_shortcode('abc') is False # too short
        assert helpers.is_valid_shortcode('abcdefg') is False # too long

    def test_generate_shortcode(self):
        assert helpers.is_valid_shortcode(helpers.generate_shortcode())

    def test_is_valid_url(self):
        assert helpers.is_valid_url('https://www.test.com')
        assert helpers.is_valid_url('http://www.test.com')
        assert helpers.is_valid_url('test.com') is False # no http / https
        assert helpers.is_valid_url('nope') is False
