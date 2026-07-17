from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsManagerOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return (request.user.is_authenticated and
                (
                        request.user.is_superuser or request.user.role=='MANAGER'
                )
                )