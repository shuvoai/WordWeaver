from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from services.pagination import CustomPageNumberPagination
from services.customize_response import customize_response
from services.custom_exceptions import InvalidRequest
from services.exception_handler import exception_handler
from services.constants import ErrorTypes
from ..serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from ..permissions import (
    IsOwner,
    CustomIsAdminUser
)

User = get_user_model()


class UserGenericViewSet(GenericViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPageNumberPagination
    search_fields = ['=email']
    ordering_fields = ['first_name', 'date_joined']
    ordering = ['-date_joined']
    lookup_field = 'pk'
    lookup_url_kwarg = 'user_id'

    def list(self, request, *args, **kwargs):
        """
        list of all users
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return customize_response(
                response,
                _('list of all users')
            )

    def create(self, request, *args, **kwargs):
        """
        create a new user
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
            return customize_response(response, _('New user created successfully'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('New user creation failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def retrieve(self, request, user_identifier=None, *args, **kwargs):
        """
        retrieve a user by user pk
        """
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            response = Response(serializer.data)
            return customize_response(response, _('User details with this pk'))
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('User retrieval failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )
        except MultipleObjectsReturned as excpt:
            return exception_handler(
                exc=excpt,
                message=_('Multiple users returned for same user pk'),
                error_type=ErrorTypes.MULTIPLE_OBJECT_RETURNED.value
            )

    def update(self, request, user_identifier=None, *args, **kwargs):
        """
        update a user details
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
            return customize_response(response, _('User details updated'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('User details update failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('User details update  failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def partial_update(self, request, user_identifier=None, *args, **kwargs):
        """
        partially update a user details
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
            return customize_response(response, _('User details partially updated'))
        except ValidationError as excpt:
            return exception_handler(
                exc=excpt,
                message=_('User details partially update failed'),
                error_type=ErrorTypes.FORM_FIELD_ERROR.value
            )

    def destroy(self, request, user_identifier=None, *args, **kwargs):
        """
        delete a user
        """
        try:
            user = self.get_object()
            user.delete()
            response = Response()
            return customize_response(response, _('User Delete Successful'))
        except Http404 as excpt:
            return exception_handler(
                exc=excpt,
                message=_('User deletion failed'),
                error_type=ErrorTypes.OBJECT_DOES_NOT_EXIST.value
            )

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['list', 'destroy', 'retrieve']:
            permission_classes += [CustomIsAdminUser]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes += [IsOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Returns the serializer class that this view requires based on
        different action
        """
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
