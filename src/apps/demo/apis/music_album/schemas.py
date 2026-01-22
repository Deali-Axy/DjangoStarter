from ninja import ModelSchema
from apps.demo.models import *


class MusicAlbumIn(ModelSchema):
    class Meta:
        model = MusicAlbum
        fields = ['name', 'year', ]


class MusicAlbumOut(ModelSchema):
    class Meta:
        model = MusicAlbum
        fields = ['id', 'is_deleted', 'created_time', 'updated_time', 'name', 'year', ]
