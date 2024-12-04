from rest_framework import serializers

from ..models import Resume, Job, JobApplication, UserProfile, CompanyProfile


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'title', 'content_json', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_content_json(self, value):
        required_sections = ['education', 'experience', 'skills']
        if not all(section in value for section in required_sections):
            raise serializers.ValidationError("필수 섹션이 누락되었습니다.")
        return value

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'user', 'job', 'resume', 'status', 'applied_at']
        read_only_fields = ['applied_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['subscription_type', 'subscription_expires', 'is_company']

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'business_registration_number', 'is_verified']