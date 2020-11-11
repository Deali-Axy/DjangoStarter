from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if "v1" in tags and operation_keys:
            # NOTE: `operation_keys` is a list like ['v1', 'user_log', 'create']
            tags[0] = operation_keys[1]

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
                'name': 'core',
                'description': '核心功能'
            }
        ]

        return swagger
