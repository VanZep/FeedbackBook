from rest_framework import permissions


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Разрешение админа или только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin)


class IsAuthorOrAdminPermission(permissions.BasePermission):
    """Разрешение амина, модератора, автора."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminPermission(permissions.BasePermission):
    """Разрешение админа."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)
