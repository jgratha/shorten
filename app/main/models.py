from datetime import datetime

from app import db


class Url(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(2000), unique=True)

    shortcodes = db.relationship(
        'Shortcode', back_populates='url'
    )

    def __repr__(self):
        return f'Url: {self.url}'


class Shortcode(db.Model):
    __tablename__ = 'shortcode'

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shortcode = db.Column(db.String(6), unique=True)

    url = db.relationship('Url', back_populates='shortcodes')
    redirects = db.relationship('Redirect', back_populates='shortcode')

    def __repr__(self):
        return f'Shortcode: {self.shortcode}'


class Redirect(db.Model):
    __tablename__ = 'redirect'

    id = db.Column(db.Integer, primary_key=True)
    shortcode_id = db.Column(db.Integer, db.ForeignKey('shortcode.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shortcode = db.relationship('Shortcode', back_populates='redirects')
