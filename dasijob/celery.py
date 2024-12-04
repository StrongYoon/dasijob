from celery import Celery
from celery.schedules import crontab

app = Celery('dasijob')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 정기적인 태스크 스케줄링
app.conf.beat_schedule = {
    'generate-daily-analytics': {
        'task': 'jobs.tasks.generate_daily_analytics',
        'schedule': crontab(hour=0, minute=0),  # 매일 자정
    },
    'generate-job-trends': {
        'task': 'jobs.tasks.generate_job_trends',
        'schedule': crontab(hour='*/6'),  # 6시간마다
    },
    'cleanup-old-analytics': {
        'task': 'jobs.tasks.cleanup_old_analytics',
        'schedule': crontab(hour=1, minute=0),  # 매일 새벽 1시
    },
}