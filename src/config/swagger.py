from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        # 处理一下swagger的文档tag，防止django-starter的接口都堆在一起
        if "django-starter" in tags and operation_keys:
            # NOTE: `operation_keys` is a list like ['v1', 'user_log', 'create']
            tags[0] = f'django-starter-{operation_keys[1]}'

        return tags


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    """
    重写 OpenAPISchemaGenerator 实现每个tag的说明文本
    参考: https://stackoverflow.com/questions/62572389/django-drf-yasg-how-to-add-description-to-tags
    """

    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)

        swagger.tags = [
            {
                'name': 'guide',
                'description': '例子代码'
            },
            {
                'name': 'django-starter-auth',
                'description': '认证'
            },
            {
                'name': 'django-starter-captcha',
                'description': '验证码'
            },
            {
                'name': 'django-starter-config',
                'description': '本地配置中心'
            },
            {
                'name': 'django-starter-oauth',
                'description': '第三方登录'
            },
        ]

        return swagger
