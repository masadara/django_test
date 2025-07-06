from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, View, DeleteView
from catalog.models import Product, Category
from .forms import ProductForm
from .services import get_prod_from_cache, get_products_by_category


# Create your views here.
def home(request):
    return render(request, "catalog/home.html")


class ContactView(View):
    def get(self, request):
        # Обрабатываем GET-запрос, возвращая форму контактов
        return render(request, "catalog/contacts.html")

    def post(self, request):
        # Обрабатываем POST-запрос, когда форма отправлена
        name = request.POST.get("name")
        number = request.POST.get("number")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! {number}, {message}")


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return get_prod_from_cache()

class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'catalog/product_detail.html'

def product_list(request):
    products = Product.objects.all()
    all_categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products, 'all_categories': all_categories})

def product_create(request):
    all_categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form, 'all_categories': all_categories})

def product_update(request, pk):
    all_categories = Category.objects.all()
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form, 'all_categories': all_categories})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    all_categories = Category.objects.all()
    if product.owner != request.user and not request.user.groups.filter(name='Модератор продуктов').exists():
        return HttpResponseForbidden()
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    return render(request, 'catalog/product_delete.html', {'product': product, 'all_categories': all_categories})

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/products/'

    def test_func(self):
        obj = self.get_object()
        return (
                obj.owner == self.request.user or
                self.request.user.groups.filter(name='Модератор продуктов').exists()
        )

class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True  # чтобы возвращался 403, если нет прав

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('/')

def product_list_by_category(request, category_id):
    all_categories = Category.objects.all()
    products = get_products_by_category(category_id)
    category = None if category_id == 0 else Category.objects.filter(id=category_id).first()

    context = {
        'all_categories': all_categories,
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/product_list_by_category.html', context)