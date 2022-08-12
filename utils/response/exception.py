# 自定义异常处理
import traceback
from typing import Dict

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework import status


def custom_handler(err: ValidationError, context: dict):
    if settings.DEBUG:
        # 调试模式下输出错误堆栈
        print(err, traceback.format_exc())

    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response: Response = exception_handler(err, context)

    if response is None:
        return Response({
            'message': f'服务器错误:{err}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        # 因为RestFramework默认的报错信息是 detail 字段，这里取出系统的报错信息
        msg = response.data.pop('detail', response.reason_phrase)
        res = {'message': msg}
        res.update(response.data)
        return Response(res, status=response.status_code, exception=True)
