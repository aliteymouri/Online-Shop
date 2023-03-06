from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign-in', views.SignInView.as_view(), name='sign-in')
]
