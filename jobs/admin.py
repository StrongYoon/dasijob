from django.contrib import admin

from .models import JobCategory, SubCategory, Job, Application

admin.site.register(JobCategory)
admin.site.register(SubCategory)
admin.site.register(Job)
admin.site.register(Application)