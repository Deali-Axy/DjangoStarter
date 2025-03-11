from typing import Optional, Union, Dict, Any, Tuple

from django.http import HttpResponse, HttpRequest
from ninja import NinjaAPI, Router
from ninja.errors import HttpError


class ResponseGenerator:
    def __init__(self, api: NinjaAPI | None = None, router: Router | None = None):
        if api:
            self.ninja_api = api
        else:
            self.ninja_api = None
        if router:
            self.ninja_router = router
        else:
            self.ninja_router = None

    def _gen_resp(
            self,
            request: HttpRequest,
            message: str,
            resp_data: Optional[dict],
            status_code: int
    ):
        if resp_data:
            data = {'detail': message, **resp_data}
        else:
            data = {'detail': message}

        if status_code >= 400:
            # 不能使用 ninja 内置的 HttpError，因为这个 HttpError 只能附带 message，导致 resp_data 传不出去
            # raise HttpError(status_code, data['detail'])
            api: NinjaAPI | None = None
            if self.ninja_api:
                api = self.ninja_api
            if self.ninja_router:
                api = self.ninja_router.api
            if not api:
                raise HttpError(status_code, 'Not available NinjaAPI instance in ResponseGenerator')

            return api.create_response(
                request,
                data,
                status=status_code
            )

        return data

    def ok(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 200)

    def forbidden(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 403)

    def bad_request(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 400)

    def not_found(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 404)

    def unauthorized(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 401)

    def error(self, request: HttpRequest, message: str, data: Optional[dict] = None):
        return self._gen_resp(request, message, data, 500)


def _gen_resp(message, resp_data: Optional[dict], status_code):
    if resp_data:
        data = {'detail': message, **resp_data}
    else:
        data = {'detail': message}

    if status_code >= 400:
        # 不能使用 ninja 内置的 HttpError，因为这个 HttpError 只能附带 message，导致 resp_data 传不出去
        # raise HttpError(status_code, data['detail'])
        # HttpResponse(data, status=status_code, content_type='application/json')
        return status_code, data

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
