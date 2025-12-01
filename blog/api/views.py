from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from accounts.models import User
from baseapp.models import Category, Blog
from .serializers import UserSerializer, CategorySerializer, BlogSerailizer

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
    serializer_class = BlogSerailizer

    def perform_create(self, serializer):
            serializer.save(author=self.request.user)
            