from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "EMPLOYEE"

class IsLeaveRequestOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.submitted_by == request.user
