from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views
from catalog.apps import CatalogConfig
from catalog.views import home, ProductListView, ProductDetailView, ContactView
from .views import product_list, product_create, product_update, product_delete
from .views import ProductUnpublishView

app_name = CatalogConfig.name

urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path('', ProductListView.as_view(), name="prod_list"),
    path('catalog/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
    path('create/', product_create, name='product_create'),
    path('update/<int:pk>/', product_update, name='product_update'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
    path('users/', include('users.urls', namespace='users')),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('products/', product_list, name='product_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('category/<int:category_id>/', views.product_list_by_category, name='products_by_category'),

]
