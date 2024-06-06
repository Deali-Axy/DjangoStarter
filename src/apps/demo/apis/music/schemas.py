from ninja import ModelSchema
from apps.demo.models import *


class MusicIn(ModelSchema):
    album_id: int

    class Meta:
        model = Music
        fields = ['name', 'singer', 'genre', 'rating', ]


class MusicOut(ModelSchema):
    class Meta:
        model = Music
        fields = ['id', 'name', 'singer', 'genre', 'rating', 'album', ]
