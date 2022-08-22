import json
from django.utils import timezone

from .models import ConfigItem


def get_str(key: str) -> str:
    queryset = ConfigItem.objects.filter(key=key)
    if queryset.exists():
        return queryset.first().value
    return ''


def set_str(key: str, value: str) -> str:
    queryset = ConfigItem.objects.filter(key=key)
    item: ConfigItem
    if queryset.exists():
        item = queryset.first()
        item.value = value
        item.updated_time = timezone.now()
        item.save()
    else:
        item = ConfigItem.objects.create(
            key=key, value=value, display_name=key
        )

    return item.value


def get_int(key: str) -> int:
    value = get_str(key)
    if len(value) > 0:
        return int(value)
    return 0


def set_int(key: str, value: int) -> int:
    value = set_str(key, str(value))
    if len(value) > 0:
        return int(value)
    return 0


def get_json(key: str) -> dict:
    value = get_str(key)
    if len(value) > 0:
        return json.loads(value)

    return {}


def set_json(key: str, value: dict) -> dict:
    value = set_str(key, json.dumps(value))
    if len(value) > 0:
        return json.loads(value)

    return {}
