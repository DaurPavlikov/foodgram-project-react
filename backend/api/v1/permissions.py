from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

    def has_permission(self, request, view):
        method = request.method
        is_auth = request.user.is_authenticated
        return (method in permissions.SAFE_METHODS
                or method in permissions.ALLOWED_METHODS and is_auth)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
