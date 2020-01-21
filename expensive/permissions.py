from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        user_type = request.user.type
        if user_type is not None and user_type.name == 'developer':
            return True

        return False
