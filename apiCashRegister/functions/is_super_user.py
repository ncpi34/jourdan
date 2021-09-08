from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):
    """
    Check if user is Super Admin to restrict access
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
