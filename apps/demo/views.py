from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes


@swagger_auto_schema(
    method='get', operation_summary='测试分页功能',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
    ])
@api_view()
def test_page(request):
    from utils.paginator import NumberPaginator
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    paginator = NumberPaginator(request.query_params.get('page_size', 10))
    return paginator.get_paginated_response({
        'data': paginator.paginate_queryset(queryset=data, request=request)
    })
