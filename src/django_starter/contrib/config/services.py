import json
from django.utils import timezone

from .models import ConfigItem


def has_key(key: str) -> bool:
    queryset = ConfigItem.objects.filter(key=key)
    return queryset.exists()


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


def get_bool(key: str) -> bool:
    value = get_str(key)
    if value == '1':
        return True
    return False


def set_bool(key: str, value: bool) -> bool:
    value = set_str(key, str('1' if value else '0'))
    return True if value == '1' else False


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
