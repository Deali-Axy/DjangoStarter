import sys
from django.views.debug import technical_500_response
from django.conf import settings


class UserBasedExceptionMiddleware(object):
    """

    1. 普通访问者看到的是友好的报错信息
    2. 管理员看到的是错误详情，以便于修复 BUG

    添加到 settings.py 中的 MIDDLEWARE_CLASSES 中，可以放到最后，这样可以看到其它中间件的 process_request的错误。

    """

    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())
