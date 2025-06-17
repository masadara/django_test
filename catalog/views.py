from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View, DeleteView
from catalog.models import Product
from .forms import ProductForm


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

class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'catalog/product_detail.html'

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list.html')  # или другой URL
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # или другой URL
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return render(request, 'catalog/product_delete.html', {'product': product})

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/products/'

    def test_func(self):
        return self.request.user.has_perm('catalog.delete_product')

class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True  # чтобы возвращался 403, если нет прав

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('/')