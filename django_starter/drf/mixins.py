from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response


class ListModelMixinExt:
    """
    List a queryset.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, name='is_paged',
                              description='是否开启分页'),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('is_paged', '1') in ['1', 'true']:
            page = self.paginate_queryset(queryset)
        else:
            page = None

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
