from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from django_starter.http.response import responses

from apps.demo.models import *
from apps.demo.apis.actor.schemas import *

router = Router(tags=['actor'])


@router.post('/actor', response=ActorOut, url_name='demo/actor/create')
def create(request, payload: ActorIn):
    item = Actor.objects.create(**payload.dict())
    return item


@router.get('/actor/{item_id}', response=ActorOut, url_name='demo/actor/retrieve')
def retrieve(request, item_id):
    item = get_object_or_404(Actor, id=item_id)
    return item


@router.get('/actor', response=List[ActorOut], url_name='demo/actor/list')
@paginate
def list_items(request):
    qs = Actor.objects.all()
    return qs


@router.put('/actor/{item_id}', response=ActorOut, url_name='demo/actor/update')
def update(request, item_id, payload: ActorIn):
    item = get_object_or_404(Actor, id=item_id)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.patch('/actor/{item_id}', response=ActorOut, url_name='demo/actor/partial_update')
def partial_update(request, item_id, payload: ActorIn):
    item = get_object_or_404(Actor, id=item_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete('/actor/{item_id}', url_name='demo/actor/destroy')
def destroy(request, item_id):
    item = get_object_or_404(Actor, id=item_id)
    item.delete()
    return responses.ok('已删除')