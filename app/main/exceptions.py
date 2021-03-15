from werkzeug.exceptions import HTTPException


class UrlNotPresentException(HTTPException):
    code = 400
    description = "Url not present"


class ShortcodeInvalidException(HTTPException):
    code = 412
    description = "The provided shortcode is invalid"


class UrlInvalidException(HTTPException):
    code = 412
    description = "The provided url is invalid"


class ShortcodeAlreadyInUseException(HTTPException):
    code = 409
    description = "Shortcode already in use"


class ShortcodeNotFoundException(HTTPException):
    code = 404
    description = "Shortcode not found"

