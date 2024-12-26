from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', UserCreateView.as_view(template_name='users/register.html'), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]