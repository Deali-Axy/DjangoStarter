from ninja.errors import HttpError


def _gen_resp(message, resp_data, status_code):
    if resp_data:
        data = {'message': message, **resp_data}
    else:
        data = {'message': message}

    if status_code >= 400:
        raise HttpError(status_code, data['message'])

    return data


def ok(message, data=None):
    return _gen_resp(message, data, 200)


def forbidden(message, data=None):
    return _gen_resp(message, data, 403)


def bad_request(message, data=None):
    return _gen_resp(message, data, 400)


def not_found(message, data=None):
    return _gen_resp(message, data, 404)


def unauthorized(message, data=None):
    return _gen_resp(message, data, 401)


def error(message, data=None):
    return _gen_resp(message, data, 500)
