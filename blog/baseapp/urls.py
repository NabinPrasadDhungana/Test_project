from django.urls import path
from .views import IndexView
from .models import Category, Blog

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
