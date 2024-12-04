from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class JobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(max_length=50, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'keyword']


# notifications/tasks.py
from celery import shared_task
from .models import JobAlert, Job


@shared_task
def check_new_jobs():
    alerts = JobAlert.objects.filter(is_active=True)
    for alert in alerts:
        new_jobs = Job.objects.filter(
            title__icontains=alert.keyword,
            created_at__gte=alert.last_checked
        )
        if new_jobs.exists():
            send_job_alert_email(alert.user, new_jobs)


# views.py에 추가
class JobAlertCreateView(LoginRequiredMixin, CreateView):
    model = JobAlert
    fields = ['keyword', 'location', 'job_type', 'salary_min']
    template_name = 'jobs/job_alert_form.html'
    success_url = reverse_lazy('jobs:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)