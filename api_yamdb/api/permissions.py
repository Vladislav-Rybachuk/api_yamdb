from .validation import CustomValidation
from rest_framework import permissions, status


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, veiw):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            if request.user.is_admin or request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False


class IsAdminModeratorAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        raise CustomValidation(
            "Требуется авторизация", 'token', status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return (
                (obj.author == request.user)
                or request.user.is_admin
                or request.user.is_moderator
            )
        raise CustomValidation(
            "Требуется авторизация", 'token', status.HTTP_401_UNAUTHORIZED)
