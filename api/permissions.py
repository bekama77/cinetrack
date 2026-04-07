from rest_framework.permissions import BasePermission

class IsOwnerOfWatchEntry(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
