from ninja import ModelSchema
from apps.demo.models import *


class MovieIn(ModelSchema):
    

    class Meta:
        model = Movie
        fields = ['title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]


class MovieOut(ModelSchema):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'year', 'rating', 'genre', 'director', 'actors', ]
