from rest_framework.permissions import BasePermission, SAFE_METHODS


class OnlyAdminCanCreateUpdateAndDeleteAnyoneCanGet(BasePermission):
    def has_permission(self, request, view):
        restricted_methods = ["POST", "PUT", "PATCH", "DELETE"]

        if request.method in SAFE_METHODS:
            return True
        elif request.method in restricted_methods:
            return request.user.is_authenticated and request.user.user_type in (
                "admin",
            )
        else:
            return False


class OnlyAdminAllowed(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ("admin",)
