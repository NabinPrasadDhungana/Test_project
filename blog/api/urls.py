from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CategoryViewSet, BlogViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categories', CategoryViewSet, basename='category')
router.register('blogs', BlogViewSet, basename='blog')
router.register('comments', CommentViewSet, basename='comment')
router.register('likes', LikeViewSet, basename='likes')

urlpatterns = [
    
]

urlpatterns += router.urls
