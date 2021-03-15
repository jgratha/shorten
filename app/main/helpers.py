import re

import shortuuid
import string

shortcode_pattern = re.compile("[a-z0-9_]{6}", re.IGNORECASE)
shortcode_alphabet = string.ascii_letters + string.digits + '_'
shortcode_shortuuid = shortuuid.ShortUUID(alphabet=shortcode_alphabet)

url_pattern = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

def is_valid_shortcode(shortcode_str: str) -> bool:
    return bool(shortcode_pattern.fullmatch(shortcode_str))

def generate_shortcode() -> str:
    return shortcode_shortuuid.random(length=6)

def is_valid_url(url_str: str):
    return bool(url_pattern.match(url_str))

def url_ends_with_slash_shortcode(url_str: str, shortcode_str: str) -> bool:
    url_str.endswith(shortcode_str)