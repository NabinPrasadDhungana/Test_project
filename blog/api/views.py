from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from accounts.models import User
from baseapp.models import Category, Blog, Comment, Like
from .serializers import UserSerializer, CategorySerializer, BlogSerializer, CommentSerializer, LikeSerializer
from .filters import BlogFilter

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [IsAdminUser()]
        
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filterset_class = BlogFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE', 'PUT']:
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        blog_id = request.data.get('blog')
        if blog_id:
            existing_like = Like.objects.filter(user=request.user, blog=blog_id).first()
            if existing_like:
                existing_like.delete()
                return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    