from django.urls import path, include
from rest_framework import routers
from .views import (
    BlogGenericViewSet,
    CommentGenericViewSet
)

blog_router = routers.DefaultRouter()
blog_router.register('', BlogGenericViewSet, 'blog')

comment_router = routers.DefaultRouter()
comment_router.register('', CommentGenericViewSet, 'comment')


urlpatterns = [
    path('blogs/', include(blog_router.urls)),
    path('comments/', include(comment_router.urls))
]
