from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from .models import Blog, Comment
from .forms import CommentForm

# Create your views here.
# class IndexView(ListView):
#     model = Blog
#     template_name = 'baseapp/index.html'
#     context_object_name = 'blogs'
#     ordering = ['-created_at']

# class BlogDetailView(FormMixin, DetailView):
#     model = Blog
#     template_name = 'baseapp/blog_detail.html'
#     context_object_name = 'blog'
#     form_class = CommentForm

#     def get_success_url(self):
#         return reverse('blog_detail', kwargs={'slug': self.object.slug})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = self.object.comments.all().order_by('-created_at')
#         context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.blog = self.object
#         if self.request.user.is_authenticated:
#             comment.user = self.request.user
#         comment.save()
#         return super().form_valid(form)