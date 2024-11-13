from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, "catalog/home.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! {number}, {message}")
    return render(request, "catalog/contacts.html")
