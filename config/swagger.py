from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if "v1" in tags and operation_keys:
            # NOTE: `operation_keys` is a list like ['v1', 'user_log', 'create']
            tags[0] = operation_keys[1]

        return tags
