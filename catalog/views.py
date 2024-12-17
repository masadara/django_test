from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from catalog.models import Product


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

# def contact(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         number = request.POST.get("number")
#         message = request.POST.get("message")
#
#         return HttpResponse(f"Спасибо, {name}! {number}, {message}")
#     return render(request, "catalog/contacts.html")

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

# def product_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'prod_list.html', context)

# def prod_detail(request, pk):
#     prod = get_object_or_404(Product, pk=pk)
#     context = {"product": prod}
#     return render(request, 'prod_detail.html', context)
