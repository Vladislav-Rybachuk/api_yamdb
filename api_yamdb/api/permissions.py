from .validation import CustomValidation
from rest_framework import permissions, status


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, veiw):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_admin
        raise CustomValidation(
            "Вы не авторизованы!", 'token', status.HTTP_401_UNAUTHORIZED)
    
    def hes_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        raise CustomValidation(
            "Вы не авторизованы!", 'token', status.HTTP_401_UNAUTHORIZED)
    

class IsAdminModeratorAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True
        raise CustomValidation(
            "Вы не авторизованы!", 'token', status.HTTP_401_UNAUTHORIZED)

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
            "Вы не авторизрваны!", 'token', status.HTTP_401_UNAUTHORIZED)
