import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import resolve
from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.exception("Unexpected error occurred")
            return self.handle_exception(e)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            return JsonResponse({
                'error': 'validation_error',
                'detail': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(exc, APIException):
            return JsonResponse({
                'error': exc.default_code,
                'detail': exc.detail
            }, status=exc.status_code)

        return JsonResponse({
            'error': 'internal_server_error',
            'detail': '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AuthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 현재 URL의 name 가져오기
        try:
            url_name = resolve(request.path_info).url_name
        except:
            url_name = None

        # 인증이 필요한 URL 패턴 목록
        protected_urls = getattr(settings, 'PROTECTED_URLS', [])
        subscription_required = getattr(settings, 'SUBSCRIPTION_REQUIRED_URLS', [])
        company_only = getattr(settings, 'COMPANY_ONLY_URLS', [])

        # 인증 체크
        if url_name in protected_urls and not request.user.is_authenticated:
            messages.error(request, '로그인이 필요한 서비스입니다.')
            return redirect(settings.LOGIN_URL)

        # 구독 체크
        if url_name in subscription_required:
            if not request.user.is_authenticated:
                messages.error(request, '로그인이 필요한 서비스입니다.')
                return redirect(settings.LOGIN_URL)
            if not hasattr(request.user, 'subscription'):
                messages.error(request, '구독이 필요한 서비스입니다.')
                return redirect('jobs:subscription_plans')

        # 기업 회원 체크
        if url_name in company_only:
            if not request.user.is_authenticated:
                messages.error(request, '로그인이 필요한 서비스입니다.')
                return redirect(settings.LOGIN_URL)
            if not hasattr(request.user, 'company_profile'):
                messages.error(request, '기업 회원만 이용 가능한 서비스입니다.')
                return redirect('jobs:main')

        return self.get_response(request)