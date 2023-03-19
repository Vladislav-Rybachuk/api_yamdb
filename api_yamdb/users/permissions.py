from api.validation import CustomValidation
from rest_framework import permissions, status


class IsAdminorSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        raise CustomValidation("Вы не авторизованы!", "Authorization",
                               status_code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return False


class IsAdministator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class AllowedForMe(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in ['GET', 'PATCH', 'DELETE']
