from django.urls import path
from . import views
from catalog.apps import CatalogConfig
from catalog.views import home

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", views.contact, name="contacts"),
]
