from rest_framework import viewsets
from rest_framework import permissions
from . import models
from . import serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
