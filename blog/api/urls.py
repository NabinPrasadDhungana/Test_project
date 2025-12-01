from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, BlogViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('blogs', BlogViewSet, basename='blog')

urlpatterns = [
    
]

urlpatterns += router.urls
