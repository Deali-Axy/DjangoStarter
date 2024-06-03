from typing import Any, Mapping

import orjson
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.renderers import JSONRenderer, BaseRenderer
from django_starter.apis import router
from apps.account.apis import router as account_router


class ORJSONRenderer(JSONRenderer):
    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        ret = {
            'code': response_status,
            'data': data,
            'success': False
        }

        if isinstance(data, dict):
            ret['message'] = data.pop('detail', '请求成功')

        if 200 <= response_status < 300:
            ret['success'] = True

        return orjson.dumps(ret, **self.json_dumps_params)


api = NinjaAPI(renderer=ORJSONRenderer())

api.add_router('django-starter', router)
api.add_router('account', account_router)