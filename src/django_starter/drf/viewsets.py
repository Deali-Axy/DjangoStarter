from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .mixins import ListModelMixinExt


class ReadOnlyModelViewSetExt(mixins.RetrieveModelMixin,
                              ListModelMixinExt,
                              GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass
