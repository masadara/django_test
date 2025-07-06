from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from config import settings
from .models import BlogPost
from .forms import BlogPostForm
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView, CreateView


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views_count += 1
        if post.views_count == 10:
            self.send_notification(post)
        post.save()
        return post

    def send_notification(self, post):
        subject = f"Поздравляем! Статья '{post.title}' достигла 10 просмотров"
        message = f"Статья '{post.title}' теперь имеет {post.views_count} просмотров."
        recipient_list = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('post_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('post_detail',
                            kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('post_list')