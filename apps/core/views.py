from django.contrib import admin

from ratelimit.decorators import ratelimit


# 覆盖默认的admin登录方法实现登录限流
@ratelimit(key='ip', rate='5/m', block=True)
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)
