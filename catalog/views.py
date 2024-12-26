from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
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

class ProductDetailView(DetailView):
    model = Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return render(request, 'catalog/product_delete.html', {'product': product})
