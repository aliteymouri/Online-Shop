from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign-in', views.SignInView.as_view(), name='sign-in'),
    path('log-out', LogoutView.as_view(next_page='home:home'), name='log-out'),
]
