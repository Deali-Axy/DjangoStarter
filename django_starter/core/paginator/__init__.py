from collections import OrderedDict

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class NumberPaginator(PageNumberPagination):
    """
    页码分页

    # 分页处理
    # 参考：https://www.cnblogs.com/liwenzhou/p/9398959.html
    paginator = NumberPaginator(request.query_params.get('page_size', 10))
    return paginator.get_paginated_response({
        'data': paginator.paginate_queryset(queryset=data, request=request, view=self)
    })
    """

    def __init__(
            self,
            page_size=10,
            page_size_query_param='page_size',
            page_query_param='page',
            max_page_size=None
    ):
        """
        初始化分页

        :param page_size: 每页显示多少条
        :param page_size_query_param: URL中每页显示条数的参数
        :param page_query_param: URL中页码的参数
        :param max_page_size: 最大页码数限制
        """
        self.page_size = page_size
        self.page_size_query_param = page_size_query_param
        self.page_query_param = page_query_param
        self.max_page_size = max_page_size

    def get_paginated_response(self, data):
        paginator: Paginator = self.page.paginator

        return Response(OrderedDict([
            ('total_item_count', paginator.count),
            ('page_count', paginator.num_pages),
            ('page_number', self.page.number),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class LimitOffsetPaginator(LimitOffsetPagination):
    """Offset分页"""
    default_limit = 1
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 999


class CursorPaginator(CursorPagination):
    """加密分页"""
    cursor_query_param = 'cursor'
    page_size = 1
    ordering = '-id'  # 重写要排序的字段
