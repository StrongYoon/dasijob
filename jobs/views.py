from datetime import timedelta

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import UpdateView

from .forms import SignUpForm, UserUpdateForm
from .models import JobCategory, Job, EmailVerification


# SignUpForm 정의
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2') 11/30


class MainPageView(ListView):
    model = JobCategory
    template_name = 'jobs/main.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_jobs'] = Job.objects.all().order_by('-created_at')[:8]
        return context

class JobSearchView(ListView):
    model = Job
    template_name = 'jobs/job_search.html'
    context_object_name = 'jobs'
    paginate_by = 12

    def get_queryset(self):
        queryset = Job.objects.all()
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(company__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        return queryset.order_by('-created_at')

class CategoryDetailView(DetailView):
    model = JobCategory
    template_name = 'jobs/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = self.object.subcategories.all()
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        subcategory_id = self.kwargs.get('subcategory_id')
        return Job.objects.filter(subcategory_id=subcategory_id).order_by('-created_at')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'jobs/signup.html'
    success_url = reverse_lazy('jobs:signup_done')  # 추가할 URL

    # def form_valid(self, form):
    #     # 폼이 유효한 경우의 처리를 위해 print 문 추가
    #     print("Form is valid!")
    #     response = super().form_valid(form)
    #     print("User created!")
    #     return response

    def form_invalid(self, form):
        # 폼이 유효하지 않은 경우의 처리를 위해 print 문 추가
        print("Form errors:", form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        # 폼이 유효한 경우의 처리를 위해 print 문 추가
        print("Form is valid!")
        response = super().form_valid(form)
        print("User created!")
        return response

        # 인증 토큰 생성
        token = get_random_string(length=32)
        EmailVerification.objects.create(
            user=user,
            token=token
        )

        # 이메일 내용 생성
        verification_url = self.request.build_absolute_uri(
            reverse('jobs:verify_email', kwargs={'token': token})
        )

        # HTML 이메일 템플릿 렌더링
        html_message = render_to_string('jobs/email/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
        })

        # 일반 텍스트 버전 생성
        plain_message = strip_tags(html_message)

        # 이메일 발송
        send_mail(
            '[다시잡] 이메일 인증을 완료해주세요',
            plain_message,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return redirect('jobs:signup_done')

class CustomLoginView(LoginView):
    template_name = 'jobs/login.html'
    next_page = 'jobs:main'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'jobs/profile_update.html'
    success_url = reverse_lazy('jobs:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # 성공 메시지 추가
        messages.success(self.request, '프로필이 성공적으로 업데이트되었습니다.')
        return response


def logout_view(request):
    logout(request)
    return redirect('jobs:main')

# class CustomLogoutView(LogoutView):
#     next_page = reverse_lazy('jobs:main')
#
#     def post(self, request, *args, **kwargs):
#         """POST 요청 처리"""
#         auth_logout(request)
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get(self, request, *args, **kwargs):
#         """GET 요청도 처리할 수 있도록 수정"""
#         return self.post(request, *args, **kwargs)

class SignupDoneView(TemplateView):
    """
    회원가입 완료 후 이메일 인증 안내 페이지를 보여주는 view
    TemplateView를 사용하는 이유: 단순히 템플릿만 보여주면 되기 때문
    """
    template_name = 'jobs/signup_done.html'


# 회원가입 뷰 수정
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 바로 저장하지 않고 user 객체만 생성
            user.is_active = False  # 이메일 인증 전까지는 계정 비활성화
            user.save()

            # 인증 토큰 생성
            token = get_random_string(length=32)
            EmailVerification.objects.create(
                user=user,
                token=token
            )

            # 인증 이메일 발송
            verification_url = f"{request.scheme}://{request.get_host()}/verify/{token}"
            send_mail(
                '이메일 인증을 완료해주세요',
                f'다음 링크를 클릭하여 인증을 완료하세요: {verification_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('verification_sent')


def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)

    if timezone.now() > verification.created_at + timedelta(days=1):
        # 인증 만료 처리: 24시간이 지났다면
        verification.delete()  # 기존 인증 정보 삭제
        return render(request, 'jobs/verification_expired.html')

    # 인증 성공 처리
    user = verification.user
    user.is_active = True  # 사용자 계정 활성화
    user.save()

    verification.is_verified = True
    verification.save()

    return redirect('jobs:verification_success')

def verification_success(request):
    """
    이메일 인증 성공 시 보여줄 view
    템플릿에서 축하 메시지와 로그인 링크를 보여줌
    """
    return render(request, 'jobs/verification_success.html')

def verification_expired(request):
    """
    이메일 인증 만료 시 보여줄 view
    재인증 안내 메시지를 보여줌
    """
    return render(request, 'jobs/verification_expired.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'jobs/password_reset_form.html'
    email_template_name = 'jobs/password_reset_email.html'
    success_url = reverse_lazy('jobs:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'jobs/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'jobs/password_reset_confirm.html'
    success_url = reverse_lazy('jobs:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'jobs/password_reset_complete.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'subcategory', 'description', 'requirements',
                 'location', 'salary', 'work_type', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '채용 공고 제목'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '회사명'
            }),
            'subcategory': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': '5',
                'placeholder': '직무 설명'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': '5',
                'placeholder': '자격 요건'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '근무지 위치'
            }),
            'salary': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '급여'
            }),
            'work_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            })
        }

class JobPostCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobPostForm
    template_name = 'jobs/job_post_form.html'
    success_url = reverse_lazy('jobs:main')

    def form_valid(self, form):
        form.instance.created_at = timezone.now()
        messages.success(self.request, '채용공고가 성공적으로 등록되었습니다.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        return context