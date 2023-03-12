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


class IsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        raise CustomValidation("Вы не авторизованы!", "Authorization",
                               status_code=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj
        return False


class IsAdministator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (view.kwargs.get('username') == 'me'
                or request.user.is_admin()
                or request.user.is_superuser)
