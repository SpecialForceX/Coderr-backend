from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer

class IsReviewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
