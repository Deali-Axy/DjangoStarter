from rest_framework import serializers
from .models import *


class CommonConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonConfig
        fields = '__all__'

