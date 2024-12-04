# jobs/permissions.py
from django.core.exceptions import PermissionDenied
from rest_framework import permissions


class IsResumeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.user == request.user


class CanAccessAnalytics(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('jobs.view_analytics')


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'company_profile')


# 데코레이터
def require_subscription(subscription_type):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("로그인이 필요합니다.")

            if not hasattr(request.user, 'subscription'):
                raise PermissionDenied("구독이 필요한 서비스입니다.")

            if request.user.subscription.type < subscription_type:
                raise PermissionDenied("상위 구독이 필요한 서비스입니다.")

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator