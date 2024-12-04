from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Resume, JobApplication, Job


class UserUpdateForm(forms.ModelForm):  # Form 대신 ModelForm 사용
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '사용자 이름'
            })
        }

class SignUpForm(UserCreationForm):  # Form 대신 UserCreationForm 상속
    email = forms.EmailField()

    class Meta:  # Meta 클래스는 클래스 내부에 있어야 함
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):  # clean_email 메서드도 클래스 내부로
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용중인 이메일입니다.')
        return email

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'education', 'experience', 'skills', 'introduction']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control'}),
            'introduction': forms.Textarea(attrs={'class': 'form-control'})
        }


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'subcategory', 'description', 'requirements',
                 'location', 'salary', 'work_type', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '채용 공고 제목'
            })
            # ... 나머지 필드들의 위젯 설정
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['user', 'job', 'resume', 'cover_letter', 'status']
        widgets = {
            'resume': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': '10',
                'placeholder': '자기소개와 지원동기를 작성해주세요.'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].queryset = Resume.objects.filter(user=user)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '아이디를 입력하세요'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        })


class JobSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '검색어를 입력하세요'
    }))

    experience = forms.ChoiceField(
        required=False,
        choices=[('', '경력선택')] + Job.EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )