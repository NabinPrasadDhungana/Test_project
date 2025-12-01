from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from accounts.models import User
from baseapp.models import Category, Blog
from .serializers import UserSerializer, CategorySerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAuthenticated]
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    