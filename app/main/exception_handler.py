import traceback

from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.main import bp

@bp.errorhandler(Exception)
def handle_exceptions(error):
    if isinstance(error, HTTPException):
        return jsonify(dict(message=error.description)), error.code,
    else:
        traceback.print_exc()
        return jsonify(dict(message='Something went wrong')), 500
