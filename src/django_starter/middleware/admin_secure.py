import ipaddress

from django.conf import settings
from django.http.response import HttpResponseForbidden


class AdminSecureMiddleware(object):
    """
    Admin 安全中间件
    用于限制可访问 admin 管理后台的IP段
    """

    admin_url = f'/{settings.URL_PREFIX}admin'

    # IP段白名单
    allow_networks = [
        ipaddress.ip_network('10.53.0.0/20'),
    ]

    # IP地址白名单
    allow_addresses = []

    @classmethod
    def get_allow_addresses(cls):
        if len(cls.allow_addresses) > 0:
            return cls.allow_addresses

        for network in cls.allow_networks:
            for ip in network:
                cls.allow_addresses.append(ip)

        return cls.allow_addresses

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        ip_addr = ipaddress.ip_address(request.META.get('REMOTE_ADDR'))

        if request.path.startswith(self.admin_url):
            if ip_addr not in self.get_allow_addresses():
                return HttpResponseForbidden()

        return response
