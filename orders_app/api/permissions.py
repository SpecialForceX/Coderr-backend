from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer

class IsBusinessUser(BasePermission):
    """
    Permission that allows access only to authenticated users.
    Object-level check ensures only the assigned business_user can modify.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
