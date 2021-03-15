from flask import request, jsonify, redirect

from app.main import bp, exceptions, repository, helpers
from app.main.dtos import ShortenRequestDto
from app.main.helpers import is_valid_shortcode, is_valid_url


@bp.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json(force=True)
    dto = ShortenRequestDto(**data)

    if not dto.url:
        raise exceptions.UrlNotPresentException
    if not is_valid_url(dto.url):
        raise exceptions.UrlInvalidException

    if dto.shortcode:
        if not is_valid_shortcode(dto.shortcode):
            raise exceptions.ShortcodeInvalidException
        if repository.does_shortcode_exist(dto.shortcode):
            raise exceptions.ShortcodeAlreadyInUseException
    else:
        dto.shortcode = helpers.generate_shortcode()

    repository.insert_shortcode(dto.shortcode, dto.url)

    return jsonify({'shortcode': dto.shortcode}), 201


@bp.route('/<shortcode>', methods=['GET'])
def get_url(shortcode):
    shortcode_model = repository.get_shortcode(shortcode)

    if not shortcode_model:
        raise exceptions.ShortcodeNotFoundException

    url = repository.get_url_for_shortcode(shortcode_model)
    assert is_valid_url(url)

    repository.register_redirect(shortcode_model)

    return redirect(url)


@bp.route('/<shortcode>/stats', methods=['GET'])
def get_stats(shortcode):
    shortcode_model = repository.get_shortcode(shortcode)

    if not shortcode_model:
        raise exceptions.ShortcodeNotFoundException

    stats = repository.get_shortcode_stats(shortcode_model)

    return jsonify(stats.dict()), 200
