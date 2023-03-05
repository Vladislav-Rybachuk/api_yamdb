from rest_framework import permissions


class IsAdministator(permissions.BasePermission):

    def has_permission(self, request, view):
        return  view.kwargs.get('username') == 'me' or request.user.is_admin()