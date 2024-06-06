from ninja import ModelSchema
from apps.demo.models import *


class ActorIn(ModelSchema):
    

    class Meta:
        model = Actor
        fields = ['name', 'birth_date', 'country', 'city', ]


class ActorOut(ModelSchema):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'birth_date', 'country', 'city', ]
