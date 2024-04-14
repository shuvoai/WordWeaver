from django.urls import path, include
from rest_framework import routers
from .views import (
    CustomAuthToken,
    InvalidateToken,
    UserGenericViewSet
)

user_router = routers.DefaultRouter()
user_router.register('', UserGenericViewSet, 'user')


urlpatterns = [
    path('users/', include(user_router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('api-invalidate-token/', InvalidateToken.as_view()),
]
