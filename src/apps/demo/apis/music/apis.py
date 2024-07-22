from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from django_starter.http.response import responses

from apps.demo.models import *
from apps.demo.apis.music.schemas import *

router = Router(tags=['music'])


@router.post('/music', response=MusicOut, url_name='demo/music/create')
def create(request, payload: MusicIn):
    item = Music.objects.create(**payload.dict())
    return item


@router.get('/music/{item_id}', response=MusicOut, url_name='demo/music/retrieve')
def retrieve(request, item_id):
    item = get_object_or_404(Music, id=item_id)
    return item


@router.get('/music', response=List[MusicOut], url_name='demo/music/list')
@paginate
def list_items(request):
    qs = Music.objects.all()
    return qs


@router.put('/music/{item_id}', response=MusicOut, url_name='demo/music/update')
def update(request, item_id, payload: MusicIn):
    item = get_object_or_404(Music, id=item_id)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.patch('/music/{item_id}', response=MusicOut, url_name='demo/music/partial_update')
def partial_update(request, item_id, payload: MusicIn):
    item = get_object_or_404(Music, id=item_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete('/music/{item_id}', url_name='demo/music/destroy')
def destroy(request, item_id):
    item = get_object_or_404(Music, id=item_id)
    item.delete()
    return responses.ok('已删除')