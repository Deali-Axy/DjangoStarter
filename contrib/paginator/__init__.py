from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class NumberPaginator(PageNumberPagination):
    """页码分页"""

    def __init__(
            self,
            page_size,
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
