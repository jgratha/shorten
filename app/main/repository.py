from sqlalchemy.sql import func

from app import db
from app.main.dtos import ShortcodeStatsDto
from app.main.models import Url, Shortcode, Redirect


def get_shortcode(shortcode_str: str) -> Shortcode:
    shortcode = Shortcode.query.filter_by(
        shortcode=shortcode_str
    ).first()
    return shortcode


def get_shortcode_stats(shortcode_model: Shortcode) -> ShortcodeStatsDto:
    last_redirect, redirect_count = (
        db.session.query(
            func.max(Redirect.created_at).label('last_redirect'),
            func.count(Redirect.id).label('redirect_count')
        )
            .join(Shortcode)
            .filter(Shortcode.shortcode == shortcode_model.shortcode)
            .first()
    )

    return ShortcodeStatsDto(
        created=shortcode_model.created_at,
        lastRedirect=last_redirect,
        redirectCount=redirect_count
    )


def does_shortcode_exist(shortcode_str: str) -> bool:
    return bool(get_shortcode(shortcode_str))


def insert_shortcode(shortcode_str: str, url_str: str):
    url = Url.query.filter_by(
        url=url_str
    ).first()
    if not url:
        url = Url(url=url_str)
        db.session.add(url)

    shortcode = Shortcode(shortcode=shortcode_str, url=url)
    db.session.add(shortcode)
    db.session.commit()


def get_url_for_shortcode(shortcode_model: Shortcode) -> str:
    return shortcode_model.url.url


def register_redirect(shortcode_model: Shortcode):
    redirect = Redirect(
        shortcode=shortcode_model
    )
    db.session.add(redirect)
    db.session.commit()
