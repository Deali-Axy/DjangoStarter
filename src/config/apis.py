from typing import Any, Mapping

import orjson
from django.conf import settings
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.renderers import JSONRenderer, BaseRenderer
from django_starter.apis import router
from apps.account.apis import router as account_router
from apps.demo.apis import router as demo_router


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


api = NinjaAPI(
    title=f'{settings.DJANGO_STARTER["project_info"]["name"]} APIs',
    description=settings.DJANGO_STARTER["project_info"]["description"],
    renderer=ORJSONRenderer(),
    urls_namespace='api',
)

api.add_router('django-starter', router)
api.add_router('account', account_router)
api.add_router('demo', demo_router)
