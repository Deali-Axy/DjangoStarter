from typing import List, Dict

from django.shortcuts import get_object_or_404
from ninja import Router

from .models import ConfigItem
from .schemas import ConfigSchema

router = Router()


@router.get('/{item_id}', response=ConfigItem)
def get_item(request, item_id: int):
    item = get_object_or_404(ConfigItem, id=item_id)
    return item


@router.get('/', response=List[ConfigSchema])
def get_list(request):
    qs = ConfigItem.objects.all()
    return qs


@router.get('/to-dict', response=Dict[str, str], summary='获取配置字典')
def to_dict(request):
    data = {}
    for item in ConfigItem.objects.all():
        data[item.key] = item.value

    return data
