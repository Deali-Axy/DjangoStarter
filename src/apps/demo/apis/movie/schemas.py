from ninja import ModelSchema
from apps.demo.models import *


class MovieIn(ModelSchema):
    

    class Meta:
        model = Movie
        fields = ['is_deleted', 'created_time', 'updated_time', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]


class MovieOut(ModelSchema):
    class Meta:
        model = Movie
        fields = ['id', 'is_deleted', 'created_time', 'updated_time', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]
