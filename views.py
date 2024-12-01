# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import JobCategory, SubCategory, Job


class JobCategoryListView(ListView):
    model = JobCategory
    template_name = "jobs/category_list.html"
    context_object_name = "categories"


class SubCategoryListView(ListView):
    model = SubCategory
    template_name = "jobs/subcategory_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(JobCategory, pk=self.kwargs["category_id"])
        return SubCategory.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.all()

        if "subcategory_id" in self.kwargs:
            queryset = queryset.filter(subcategory_id=self.kwargs["subcategory_id"])

        work_type = self.request.GET.get("work_type")
        if work_type:
            queryset = queryset.filter(work_type=work_type)

        location = self.request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset.order_by("-created_at")


class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"


# urls.py
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.JobCategoryListView.as_view(), name="category-list"),
    path(
        "category/<int:category_id>/",
        views.SubCategoryListView.as_view(),
        name="subcategory-list",
    ),
    path(
        "subcategory/<int:subcategory_id>/jobs/",
        views.JobListView.as_view(),
        name="job-list",
    ),
    path("job/<int:pk>/", views.JobDetailView.as_view(), name="job-detail"),
]
