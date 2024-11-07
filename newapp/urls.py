from django.urls import path
from . import views
from newapp.apps import NewappConfig
from newapp.views import home

app_name = NewappConfig.name

urlpatterns = [
    path('', views.home, name='home')
]