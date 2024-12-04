import json
from datetime import timedelta

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
from django.db.models import Q, Count, Avg
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import UpdateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .api.serializers import ResumeSerializer
from .forms import SignUpForm, UserUpdateForm, ResumeForm, CustomAuthenticationForm, JobPostForm, JobSearchForm
from .models import (JobCategory, Job, EmailVerification, Resume, Notification,
                     SubCategory, JobApplication, JobTrend, BookmarkedJob,
                     Community, Mentoring, CompanyReview)


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'jobs/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

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
    template_name = 'jobs/search_results.html'
    context_object_name = 'jobs'
    paginate_by = 9

    def get_queryset(self):
        queryset = Job.objects.all()
        form = JobSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data.get('search'):
                search_query = form.cleaned_data['search']
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(company__icontains=search_query) |
                    Q(description__icontains=search_query)
                )

            if form.cleaned_data.get('experience'):
                experience = form.cleaned_data['experience']
                if experience:
                    queryset = queryset.filter(experience_required=experience)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JobSearchForm(self.request.GET)
        return context

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
        queryset = Job.objects.all()

        # 카테고리 필터링
        subcategory_id = self.kwargs.get('subcategory_id')
        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        # 검색 필터링
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(company__icontains=search) |
                Q(description__icontains=search)
            )

        # 지역 필터링
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        # 경력 필터링
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience_required__icontains=experience)

        # 정렬
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'salary':
            queryset = queryset.order_by('-salary')
        elif sort == 'deadline':
            queryset = queryset.order_by('deadline')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory_id = self.kwargs.get('subcategory_id')
        if subcategory_id:
            context['subcategory'] = get_object_or_404(SubCategory, id=subcategory_id)
            context['category_name'] = context['subcategory'].name
        else:
            context['category_name'] = "전체 채용정보"

        # 현재 적용된 필터 값들 전달
        context['current_search'] = self.request.GET.get('search', '')
        context['current_location'] = self.request.GET.get('location', '')
        context['current_experience'] = self.request.GET.get('experience', '')
        context['current_sort'] = self.request.GET.get('sort', 'latest')

        return context


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
    form_class = CustomAuthenticationForm
    template_name = 'jobs/login.html'

    def form_valid(self, form):
        # 로그인 시도 횟수 체크
        username = form.cleaned_data.get('username')
        attempts = self.request.session.get('login_attempts', 0)

        if attempts >= 5:  # 5회 이상 실패시
            minutes_locked = 30
            messages.error(
                self.request,
                f'너무 많은 로그인 시도가 있었습니다. {minutes_locked}분 후에 다시 시도해주세요.'
            )
            return self.form_invalid(form)

        # 성공시 시도 횟수 초기화
        self.request.session['login_attempts'] = 0
        return super().form_valid(form)

    def form_invalid(self, form):
        # 실패시 시도 횟수 증가
        attempts = self.request.session.get('login_attempts', 0)
        self.request.session['login_attempts'] = attempts + 1

        return super().form_invalid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'jobs/profile_update.html'
    success_url = reverse_lazy('jobs:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['email'].widget.attrs.update({'class': 'form-control'})
        form.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        form.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
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

class AllJobsListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        return Job.objects.all().order_by('-created_at')


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

class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'jobs/resume_form.html'
    success_url = reverse_lazy('jobs:resume_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '이력서가 성공적으로 등록되었습니다.')
        return super().form_valid(form)

class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'jobs/resume_list.html'
    context_object_name = 'resumes'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeDetailView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'jobs/resume_detail.html'
    context_object_name = 'resume'

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'jobs/resume_form.html'
    success_url = reverse_lazy('jobs:resume_list')

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '이력서가 성공적으로 수정되었습니다.')
        return super().form_valid(form)


from django.views.generic import ListView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'total_applications': JobApplication.objects.filter(user=user).count(),
            'in_progress': JobApplication.objects.filter(user=user, status='pending').count(),
            'upcoming_interviews': JobApplication.objects.filter(user=user, status='interview').count(),
            'saved_jobs': Job.objects.filter(bookmarks=user).count(),
            'recent_applications': JobApplication.objects.filter(user=user).order_by('-applied_at')[:5],
            'recommended_jobs': Job.objects.all()[:4],  # 추천 로직은 나중에 구현
            'completed_resumes': Resume.objects.filter(user=user, is_completed=True).count(),
            'draft_resumes': Resume.objects.filter(user=user, is_completed=False).count(),
            'upcoming_deadlines': Job.objects.filter(deadline__gte=timezone.now()).order_by('deadline')[:5],
        })
        return context

class ResumePreviewView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'jobs/resume_preview.html'
    context_object_name = 'resume'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completion_rate'] = self.object.calculate_completion_rate()
        return context


class JobAnalyticsView(TemplateView):
    template_name = 'jobs/job_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', '30')

        # 기본 통계
        context['total_jobs'] = Job.objects.count()
        context['avg_salary'] = Job.objects.aggregate(Avg('salary'))['salary__avg']
        context['avg_experience'] = Job.objects.aggregate(Avg('experience_required'))['experience_required__avg']
        context['avg_applicants'] = \
        context['avg_applicants'] = JobApplication.objects.values('job').annotate(count=Count('id')).aggregate(Avg('count'))['count__avg']

        # 채용 추이 데이터
        trends = Job.objects.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        context['job_trends_data'] = json.dumps([item['count'] for item in trends])
        context['job_trends_labels'] = json.dumps([item['date'].strftime('%Y-%m-%d') for item in trends])

        # 직종별 데이터
        categories = Job.objects.values('category__name').annotate(count=Count('id'))
        context['category_data'] = json.dumps([item['count'] for item in categories])
        context['category_labels'] = json.dumps([item['category__name'] for item in categories])

        # 지역별 데이터
        regions = Job.objects.values('location').annotate(count=Count('id'))
        context['region_data'] = json.dumps([item['count'] for item in regions])
        context['region_labels'] = json.dumps([item['location'] for item in regions])

        # 인기 기술 스택
        context['popular_skills'] = Job.objects.values('required_skills').annotate(
            count=Count('id')
        ).order_by('-count')[:9]

        return context


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'jobs/login.html'

    def form_valid(self, form):
        # 로그인 시도 횟수 체크
        username = form.cleaned_data.get('username')
        attempts = self.request.session.get('login_attempts', 0)

        if attempts >= 5:  # 5회 이상 실패시
            minutes_locked = 30
            messages.error(
                self.request,
                f'너무 많은 로그인 시도가 있었습니다. {minutes_locked}분 후에 다시 시도해주세요.'
            )
            return self.form_invalid(form)

        # 성공시 시도 횟수 초기화
        self.request.session['login_attempts'] = 0
        return super().form_valid(form)

    def form_invalid(self, form):
        # 실패시 시도 횟수 증가
        attempts = self.request.session.get('login_attempts', 0)
        self.request.session['login_attempts'] = attempts + 1

        return super().form_invalid(form)

class ModernDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/modern_dashboard.html'

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/analytics_dashboard.html'

class ResumeBuilderView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/resume_builder.html'

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def save_builder_content(self, request):
        resume = Resume.objects.get(id=request.data.get('id'))
        resume.content_json = request.data.get('content')
        resume.save()
        return Response({'status': 'success'})

class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def dashboard_stats(self, request):
        # 대시보드에 필요한 통계 데이터 반환
        return Response({
            'job_trends': [],
            'category_stats': [],
            'location_stats': [],
            'salary_stats': {}
        })

class JobApplicationView(LoginRequiredMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        # 지원 완료 후 실시간 업데이트 발송
        send_application_update(self.request.user.id, {
            'application_id': self.object.id,
            'status': 'applied',
            'job_title': self.object.job.title
        })
        return response

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def save_draft(self, request, pk=None):
        resume = self.get_object()
        resume.content_json = request.data.get('content')
        resume.is_draft = True
        resume.save()
        return Response({'status': 'draft saved'})

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        resume = self.get_object()
        resume.is_draft = False
        resume.save()
        return Response({'status': 'published'})


class AnalyticsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """대시보드용 통계 데이터"""
        today = timezone.now().date()
        analytics = JobAnalytics.objects.filter(date=today).first()

        if not analytics:
            analytics = JobAnalytics.generate_daily_stats()

        return Response({
            'total_jobs': analytics.total_jobs,
            'total_applications': analytics.total_applications,
            'category_stats': analytics.category_stats,
            'location_stats': analytics.location_stats,
            'salary_stats': analytics.salary_stats
        })

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """트렌드 데이터"""
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)

        trends = JobTrend.objects.filter(
            date__gte=start_date
        ).order_by('date').values()

        return Response(list(trends))

    @action(detail=False, methods=['get'])
    def category_analysis(self, request):
        """카테고리별 상세 분석"""
        analytics = JobAnalytics.objects.latest('date')
        category_data = analytics.category_stats

        for category, count in category_data.items():
            category_data[category] = {
                'count': count,
                'avg_salary': analytics.salary_stats['by_category'].get(category, 0),
                'applications': JobApplication.objects.filter(
                    job__subcategory__category__name=category
                ).count()
            }

        return Response(category_data)


class JobAlertListView(LoginRequiredMixin, ListView):
    model = Notification  # 또는 적절한 모델
    template_name = 'jobs/job_alerts.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            notification_type='new_job'
        )

class BookmarkedJobsView(LoginRequiredMixin, ListView):
    model = BookmarkedJob
    template_name = 'jobs/bookmarked_jobs.html'
    context_object_name = 'bookmarks'

    def get_queryset(self):
        return BookmarkedJob.objects.filter(user=self.request.user)

class CommunityListView(LoginRequiredMixin, ListView):
    model = Community
    template_name = 'jobs/community_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Community.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MentoringView(LoginRequiredMixin, ListView):
    model = Mentoring
    template_name = 'jobs/mentoring.html'
    context_object_name = 'mentoring_sessions'

    def get_queryset(self):
        user = self.request.user
        return Mentoring.objects.filter(
            Q(mentor=user) | Q(mentee=user)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CompanyReviewListView(LoginRequiredMixin, ListView):
    model = CompanyReview
    template_name = 'jobs/company_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        company_id = self.kwargs.get('pk')
        return CompanyReview.objects.filter(company_id=company_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        return context

