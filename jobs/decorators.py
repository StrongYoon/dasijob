from functools import wraps

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def subscription_required(subscription_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, '로그인이 필요한 서비스입니다.')
                return redirect('jobs:login')

            if not hasattr(request.user, 'userprofile'):
                messages.error(request, '프로필 설정이 필요합니다.')
                return redirect('jobs:profile_setup')

            if not request.user.userprofile.check_subscription(subscription_type):
                messages.warning(
                    request,
                    f'{subscription_type} 이상의 구독이 필요한 서비스입니다.'
                )
                return redirect('jobs:subscription_plans')

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def company_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, '로그인이 필요합니다.')
            return redirect('jobs:login')

        if not hasattr(request.user, 'companyprofile'):
            messages.error(request, '기업 회원만 이용 가능한 서비스입니다.')
            return redirect('jobs:main')

        if not request.user.companyprofile.is_verified:
            messages.warning(request, '기업 인증이 필요한 서비스입니다.')
            return redirect('jobs:company_verification')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def permission_required(permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("로그인이 필요합니다.")

            if not UserPermission.objects.filter(
                    user=request.user,
                    permission_name=permission_name
            ).exists():
                raise PermissionDenied("접근 권한이 없습니다.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator