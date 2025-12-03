from django.urls import path
from .views import IndexView#, BlogDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
#     path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]
