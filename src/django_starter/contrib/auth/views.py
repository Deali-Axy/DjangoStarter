from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django_starter.http.response import responses
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


@swagger_auto_schema(method='get', operation_summary='获取当前用户信息')
@api_view()
@permission_classes([permissions.IsAuthenticated])
def get_current_user_info(request):
    user = UserSerializer(request.user).data
    profile = {}
    if UserProfile.objects.filter(user=request.user).exists():
        profile = UserProfileSerializer(request.user.profile).data

    return responses.ok('获取当前用户信息', {
        'user': user,
        'profile': profile,
    })
