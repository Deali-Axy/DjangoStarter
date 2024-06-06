from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from django_starter.http.response import responses

from apps.demo.models import *
from apps.demo.apis.movie.schemas import *

router = Router(tags=['movie'])


@router.post('/movie', response=MovieOut, url_name='demo/movie/create')
def create(request, payload: MovieIn):
    item = Movie.objects.create(**payload.dict())
    return item


@router.get('/movie/{item_id}', response=MovieOut, url_name='demo/movie/retrieve')
def retrieve(request, item_id):
    item = get_object_or_404(Movie, id=item_id)
    return item


@router.get('/movie', response=List[MovieOut], url_name='demo/movie/list')
@paginate
def list_items(request):
    qs = Movie.objects.all()
    return qs


@router.put('/movie/{item_id}', response=MovieOut, url_name='demo/movie/update')
def update(request, item_id, payload: MovieIn):
    item = get_object_or_404(Movie, id=item_id)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.patch('/movie/{item_id}', response=MovieOut, url_name='demo/movie/partial_update')
def partial_update(request, item_id, payload: MovieIn):
    item = get_object_or_404(Movie, id=item_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete('/movie/{item_id}', url_name='demo/movie/destroy')
def destroy(request, item_id):
    item = get_object_or_404(Movie, id=item_id)
    item.delete()
    return responses.ok('已删除')