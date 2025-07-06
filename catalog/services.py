from django.core.cache import cache
from django.shortcuts import get_object_or_404

from config.settings import CACHES_ENABLED
from catalog.models import Product, Category


def get_prod_from_cache():
    if not CACHES_ENABLED:
        return Product.objects.all()
    key = "prod_list"
    prods = cache.get(key)
    if prods is not None:
        return prods
    prods = Product.objects.all()
    cache.set(key, prods)
    return prods

def get_products_by_category(category_id):
    if category_id == 0:
        products = Product.objects.filter(category__isnull=True, is_published=True)
    else:
        products = Product.objects.filter(category_id=category_id, is_published=True)
    return products