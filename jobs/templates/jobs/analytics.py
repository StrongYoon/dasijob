# jobs/analytics.py
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate

from .models import Job, JobApplication, JobCategory


class JobAnalytics:
    @staticmethod
    def get_job_trends(days=30):
        return Job.objects.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

    @staticmethod
    def get_popular_categories():
        return JobCategory.objects.annotate(
            job_count=Count('jobs')
        ).order_by('-job_count')

    @staticmethod
    def get_application_stats():
        return JobApplication.objects.aggregate(
            total_applications=Count('id'),
            avg_applications_per_job=Count('id') / Count('job', distinct=True),
            success_rate=Count('id', filter=Q(status='HIRED')) / Count('id') * 100
        )

    @staticmethod
    def get_salary_analysis():
        return Job.objects.aggregate(
            avg_salary=Avg('salary'),
            min_salary=Min('salary'),
            max_salary=Max('salary')
        )


# jobs/views.py에 추가
class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'jobs/analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analytics = JobAnalytics()

        context.update({
            'job_trends': analytics.get_job_trends(),
            'popular_categories': analytics.get_popular_categories(),
            'application_stats': analytics.get_application_stats(),
            'salary_analysis': analytics.get_salary_analysis(),
        })
        return context