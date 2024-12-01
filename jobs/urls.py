from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('jobs/<int:subcategory_id>/', views.JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('search/', views.JobSearchView.as_view(), name='job-search'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/done/', views.SignupDoneView.as_view(), name='signup_done'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('verify/success/', views.verification_success, name='verification_success'),
    path('verify/expired/', views.verification_expired, name='verification_expired'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', views.ProfileView.as_view(), name='profile'),  # 프로필 보기
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),  # 프로필 수정
    path('job/create/', views.JobPostCreateView.as_view(), name='job-create'),
]
