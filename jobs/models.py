from django.contrib.auth import get_user_model
from django.db import models

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


