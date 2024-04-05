from ninja import ModelSchema

from .models import ConfigItem


class ConfigSchema(ModelSchema):
    class Meta:
        model = ConfigItem
        fields = "__all__"
