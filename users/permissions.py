from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwner(BasePermission):
    message = _('You are not the owner of this object')
    code = 403

    def has_object_permission(self, request, view, obj):
        breakpoint()
        return request.user == obj


class CustomIsAdminUser(IsAdminUser):
    message = _('Only site staffs can perform this action')
    code = 403
