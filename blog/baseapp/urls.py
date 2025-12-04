from django.urls import path
from .views import IndexView, BlogDetailView, CategoryListView, CategoryBlogListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryBlogListView.as_view(), name='category_blog_list'),
]
