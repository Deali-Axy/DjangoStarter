from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from django_starter.http.response import responses

from apps.demo.models import *
from apps.demo.apis.music_album.schemas import *

router = Router(tags=['music_album'])


@router.post('/music_album', response=MusicAlbumOut, url_name='demo/music_album/create')
def create(request, payload: MusicAlbumIn):
    item = MusicAlbum.objects.create(**payload.dict())
    return item


@router.get('/music_album/{item_id}', response=MusicAlbumOut, url_name='demo/music_album/retrieve')
def retrieve(request, item_id):
    item = get_object_or_404(MusicAlbum, id=item_id)
    return item


@router.get('/music_album', response=List[MusicAlbumOut], url_name='demo/music_album/list')
@paginate
def list_items(request):
    qs = MusicAlbum.objects.all()
    return qs


@router.put('/music_album/{item_id}', response=MusicAlbumOut, url_name='demo/music_album/update')
def update(request, item_id, payload: MusicAlbumIn):
    item = get_object_or_404(MusicAlbum, id=item_id)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.patch('/music_album/{item_id}', response=MusicAlbumOut, url_name='demo/music_album/partial_update')
def partial_update(request, item_id, payload: MusicAlbumIn):
    item = get_object_or_404(MusicAlbum, id=item_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete('/music_album/{item_id}', url_name='demo/music_album/destroy')
def destroy(request, item_id):
    item = get_object_or_404(MusicAlbum, id=item_id)
    item.delete()
    return responses.ok('已删除')