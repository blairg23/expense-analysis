from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        if request.user.type.name == 'developer':
            return True

        return False
