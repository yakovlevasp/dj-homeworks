"""
Классы разделения доступа
"""
from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    """
    Разделение доступа на уровне объекта, позволяет редактировать объект только админ или владельцам
    """
    def has_object_permission(self, request, view, obj):
        """
        Проверка доступа для объекта
        """
        if request.user.is_staff:
            return True

        owner = getattr(obj, 'creator', getattr(obj, 'user', None))
        return owner == request.user
