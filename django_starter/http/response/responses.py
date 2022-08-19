from rest_framework import status
from rest_framework.response import Response


def _gen_resp(message, resp_data, status_code):
    if resp_data:
        data = {'message': message, **resp_data}
    else:
        data = {'message': message}
    return Response(
        data,
        status=status_code
    )


def ok(message, data=None):
    return _gen_resp(message, data, status.HTTP_200_OK)


def bad_request(message, data=None):
    return _gen_resp(message, data, status.HTTP_400_BAD_REQUEST)


def not_found(message, data=None):
    return _gen_resp(message, data, status.HTTP_404_NOT_FOUND)


def unauthorized(message, data=None):
    return _gen_resp(message, data, status.HTTP_401_UNAUTHORIZED)
