from django.contrib import admin

from .models import JobCategory, SubCategory, Job, JobApplication

admin.site.register(JobCategory)
admin.site.register(SubCategory)
admin.site.register(Job)
admin.site.register(JobApplication)