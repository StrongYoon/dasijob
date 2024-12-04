from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ResumeSerializer, JobSerializer, JobApplicationSerializer
)
from ..models import Resume, Job, JobApplication
from ..permissions import IsResumeOwner


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsResumeOwner]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def save_draft(self, request, pk=None):
        resume = self.get_object()
        resume.content_json = request.data.get('content')
        resume.is_draft = True
        resume.save()
        return Response({'status': 'draft saved'})


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Job.objects.all()
        category = self.request.query_params.get('category', None)
        location = self.request.query_params.get('location', None)

        if category:
            queryset = queryset.filter(subcategory__category__name=category)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)