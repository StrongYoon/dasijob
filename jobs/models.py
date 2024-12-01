from django.contrib.auth.models import User
from django.db import models


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


class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '검토중'),
        ('ACCEPTED', '서류합격'),
        ('INTERVIEW', '면접대기'),
        ('HIRED', '최종합격'),
        ('REJECTED', '불합격'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)