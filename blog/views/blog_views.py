from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from services.customize_response import customize_response
from services.exception_handler import exception_handler
from services.constants import ErrorTypes
from ..serializers import (
    BlogSerializer,
    BlogCreateSerializer,
    BlogUpdateSerializer,
)
from ..permissions import (
    IsBlogPostOwner
)
from users.permissions import (
    CustomIsAdminUser
)
from blog.models import (
    Blog
)

User = get_user_model()


class BlogGenericViewSet(GenericViewSet):
    queryset = Blog.objects.all()
    pagination_class = CustomPageNumberPagination
    search_fields = ['=user']
    ordering_fields = ['user', 'creation_date']
    ordering = ['-creation_date']
    lookup_field = 'pk'
    lookup_url_kwarg = 'blog_id'

    def list(self, request, *args, **kwargs):
        """
        list of all blogs
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return customize_response(
                response,
                _('list of all blogs')
            )

    def create(self, request, *args, **kwargs):
        """
        create a new blog
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
            return customize_response(response, _('New blog created successfully'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('New blog created failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def retrieve(self, request, *args, **kwargs):
        """
        retrieve a blog by blog pk
        """
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            response = Response(serializer.data)
            return customize_response(response, _('blog details with this pk'))
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('blog retrieval failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )
        except MultipleObjectsReturned as excpt:
            return exception_handler(
                exc=excpt,
                message=_('Multiple blog returned for same blog pk'),
                error_type=ErrorTypes.MULTIPLE_OBJECT_RETURNED.value
            )

    def update(self, request, user_identifier=None, *args, **kwargs):
        """
        update a blog details
        """
        try:
            user = self.get_object()
            serializer = self.get_serializer(
                user,
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response(serializer.data)
            return customize_response(response, _('blog details updated'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('blog details update failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('blog details update  failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def partial_update(self, request, user_identifier=None, *args, **kwargs):
        """
        partially update a blog details
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response(serializer.data)
            return customize_response(response, _('blog details partially updated'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('blog details partially update failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def destroy(self, request, user_identifier=None, *args, **kwargs):
        """
        delete a blog
        """
        try:
            user = self.get_object()
            user.delete()
            response = Response(status=status.HTTP_204_NO_CONTENT)
            return customize_response(response, _('blog Delete Successful'))
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('blog deletion failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    @action(methods=['get'], detail=False, url_path='auth-user-blogs')
    def auth_user_blogs(self, request, *args, **kwargs):
        """
        list of all blog posts for the authenticated user
        """
        queryset = self.filter_queryset(
            self.get_queryset()).filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return customize_response(
                response,
                'list of all rewards for the authenticated user'
            )
        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)
        return customize_response(response, 'list of all rewards for the authenticated user')

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['list', 'retrieve']:
            permission_classes += [CustomIsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes += [IsBlogPostOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Returns the serializer class that this view requires based on
        different action
        """
        if self.action in ['list', 'retrieve', 'auth_user_blogs']:
            return BlogSerializer
        elif self.action == 'create':
            return BlogCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BlogUpdateSerializer
