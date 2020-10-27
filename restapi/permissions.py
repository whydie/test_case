from rest_framework.permissions import BasePermission


class HasActiveSubscription(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.has_active_subscription()
