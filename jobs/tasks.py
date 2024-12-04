from celery import shared_task
from django.utils import timezone

from .models import JobAnalytics, JobTrend


@shared_task
def generate_daily_analytics():
    """일일 채용 통계 생성"""
    JobAnalytics.generate_daily_stats()


@shared_task
def generate_job_trends():
    """채용 트렌드 데이터 생성"""
    today = timezone.now().date()

    # 오늘의 통계 계산
    total_jobs = Job.objects.count()
    total_applications = JobApplication.objects.count()
    active_users = JobApplication.objects.values('user').distinct().count()

    avg_applications = (
        total_applications / total_jobs if total_jobs > 0 else 0
    )

    JobTrend.objects.update_or_create(
        date=today,
        defaults={
            'job_count': total_jobs,
            'application_count': total_applications,
            'active_users': active_users,
            'average_applications_per_job': avg_applications
        }
    )


@shared_task
def cleanup_old_analytics():
    """90일 이상 된 분석 데이터 삭제"""
    cutoff_date = timezone.now().date() - timezone.timedelta(days=90)
    JobAnalytics.objects.filter(date__lt=cutoff_date).delete()
    JobTrend.objects.filter(date__lt=cutoff_date).delete()