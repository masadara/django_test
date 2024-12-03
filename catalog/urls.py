from django.urls import path
from . import views
from catalog.apps import CatalogConfig
from catalog.views import home, product_list, prod_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", views.contact, name="contacts"),
    path('', product_list, name="prod_list"),
    path('catalog/<int:pk>', prod_detail, name="prod_detail")
]
