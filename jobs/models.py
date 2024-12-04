from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('application', '지원 결과'),
        ('new_job', '새로운 채용공고'),
        ('interview', '면접 제안'),
        ('deadline', '마감 임박'),
        ('system', '시스템 공지')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Job Categories"


class SubCategory(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Sub Categories"


class Job(models.Model):
    WORK_TYPE_CHOICES = [
        ('FULL', '전일제'),
        ('PART', '시간제'),
        ('TEMP', '일용직'),
        ('FREE', '프리랜서'),
    ]

    EXPERIENCE_CHOICES = [
        (0, '경력무관'),
        (1, '1년 이상'),
        (3, '3년 이상'),
        (5, '5년 이상'),
        (7, '7년 이상'),
        (10, '10년 이상')
    ]

    experience_required = models.IntegerField(
        choices=EXPERIENCE_CHOICES,
        default=0,
        verbose_name='필요 경력'
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    work_type = models.CharField(max_length=4, choices=WORK_TYPE_CHOICES)
    is_senior_friendly = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return self.title


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    education = models.TextField()
    experience = models.TextField()
    skills = models.TextField()
    introduction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_json = models.JSONField(null=True, blank=True)  # 드래그 앤 드롭 이력서 내용
    template_type = models.CharField(max_length=50, default='basic')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}의 이력서 - {self.title}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('APPLIED', '지원완료'),
        ('PENDING', '검토중'),
        ('ACCEPTED', '서류합격'),
        ('INTERVIEW', '면접대기'),
        ('HIRED', '최종합격'),
        ('REJECTED', '불합격'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    cover_letter = models.TextField(verbose_name='자기소개서')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'job']  # 한 사용자가 같은 공고에 중복 지원 방지
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.username} - {self.job.title} 지원"

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# models.py에 추가
class ResumeTemplate(models.Model):
    title = models.CharField(max_length=100)
    content = models.JSONField()
    category = models.CharField(max_length=50)


class ApplicationTracking(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    status_history = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)


class BookmarkedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'job']


class CompanyReview(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    content = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Community(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')


class Mentoring(models.Model):
    mentor = models.ForeignKey(User, related_name='mentoring_sessions', on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, related_name='mentee_sessions', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class JobAnalytics(models.Model):
    date = models.DateField(unique=True)
    total_jobs = models.IntegerField(default=0)
    total_applications = models.IntegerField(default=0)
    category_stats = models.JSONField(default=dict)
    location_stats = models.JSONField(default=dict)
    salary_stats = models.JSONField(default=dict)

    class Meta:
        ordering = ['-date']

    @classmethod
    def generate_daily_stats(cls):
        today = timezone.now().date()

        # 카테고리별 통계
        category_stats = dict(Job.objects.values('subcategory__category__name')
                              .annotate(count=Count('id'))
                              .values_list('subcategory__category__name', 'count'))

        # 지역별 통계
        location_stats = dict(Job.objects.values('location')
                              .annotate(count=Count('id'))
                              .values_list('location', 'count'))

        # 급여 통계
        salary_stats = {
            'avg': Job.objects.aggregate(Avg('salary'))['salary__avg'],
            'by_category': dict(Job.objects.values('subcategory__category__name')
                                .annotate(avg_salary=Avg('salary'))
                                .values_list('subcategory__category__name', 'avg_salary'))
        }

        analytics, _ = cls.objects.update_or_create(
            date=today,
            defaults={
                'total_jobs': Job.objects.count(),
                'total_applications': JobApplication.objects.count(),
                'category_stats': category_stats,
                'location_stats': location_stats,
                'salary_stats': salary_stats
            }
        )
        return analytics

class JobTrend(models.Model):
    date = models.DateField(unique=True)
    job_count = models.IntegerField(default=0)
    application_count = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    average_applications_per_job = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-date']

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    business_registration_number = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    verification_documents = models.FileField(
        upload_to='company_verifications/',
        null=True,
        blank=True
    )


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_name = models.CharField(max_length=100)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='granted_permissions'
    )

    class Meta:
        unique_together = ['user', 'permission_name']

class UserProfile(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('FREE', '무료'),
        ('BASIC', '기본'),
        ('PREMIUM', '프리미엄'),
        ('ENTERPRISE', '기업용')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='FREE'
    )
    subscription_expires = models.DateTimeField(null=True, blank=True)
    is_company = models.BooleanField(default=False)
    login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)

    def check_subscription(self, required_level):
        subscription_levels = {
            'FREE': 0,
            'BASIC': 1,
            'PREMIUM': 2,
            'ENTERPRISE': 3
        }
        return subscription_levels.get(self.subscription_type, 0) >= subscription_levels.get(required_level, 0)

    def is_subscription_active(self):
        if self.subscription_type == 'FREE':
            return True
        return self.subscription_expires and self.subscription_expires > timezone.now()
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    level = models.IntegerField()
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name