from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, IsAdminUser


class IsBlogPostOwner(BasePermission):
    message = _('You are not the owner of this blog post')
    code = 403

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class CustomIsAdminUser(IsAdminUser):
    message = _('Only site staffs can perform this action')
    code = 403


class IsCommentOwner(BasePermission):
    message = _('You are not the owner of this comment')
    code = 403

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
