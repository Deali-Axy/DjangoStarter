from rest_framework import serializers
from .models import *


class CommonConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigItem
        fields = '__all__'

