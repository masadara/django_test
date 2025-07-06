from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию на нашем сайте.',
            'nfuumo@mail.ru',
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Регистрация прошла успешно! Вы вошли в систему.")
        return super().form_valid(form)
