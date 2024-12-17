from django.urls import path
from . import views
from catalog.apps import CatalogConfig
from catalog.views import home, ProductListView, ProductDetailView, ContactView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path('', ProductListView.as_view(), name="prod_list"),
    path('catalog/<int:pk>', ProductDetailView.as_view(), name="prod_detail")
]
