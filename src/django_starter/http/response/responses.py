from typing import Optional

from django.http import HttpResponse
from ninja.errors import HttpError


def _gen_resp(message, resp_data: Optional[dict], status_code):
    if resp_data:
        data = {'detail': message, **resp_data}
    else:
        data = {'detail': message}

    if status_code >= 400:
        # 不能使用 ninja 内置的 HttpError，因为这个 HttpError 只能附带 message，导致 resp_data 传不出去
        # raise HttpError(status_code, data['detail'])
        HttpResponse(data, status=status_code, content_type='application/json')

    return data


def ok(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 200)


def forbidden(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 403)


def bad_request(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 400)


def not_found(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 404)


def unauthorized(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 401)


def error(message: str, data: Optional[dict] = None):
    return _gen_resp(message, data, 500)
