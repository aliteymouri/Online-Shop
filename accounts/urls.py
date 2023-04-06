from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('log-out', LogoutView.as_view(next_page='home:home'), name='log-out'),

    path('check-otp', CheckOtpView.as_view(), name='check-otp'),

    path('personal-info/', PersonalInfoView.as_view(), name='personal-info'),
]
