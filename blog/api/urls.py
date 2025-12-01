from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    
]

urlpatterns += router.urls
