from ninja import ModelSchema

from .models import ConfigItem


class ConfigItemOut(ModelSchema):
    class Meta:
        model = ConfigItem
        fields = ['key', 'value', 'display_name']
