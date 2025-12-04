from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from .models import Blog, Comment
from .forms import CommentForm

# Create your views here.
class IndexView(ListView):
    model = Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['likes_count'] = self.object.likes.count()
        # Check if current user has liked this post
        if self.request.user.is_authenticated:
            context['user_has_liked'] = self.object.likes.filter(user=self.request.user).exists()
        else:
            context['user_has_liked'] = False
        return context