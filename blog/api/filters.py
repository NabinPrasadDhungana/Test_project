import django_filters
from accounts.models import User
from baseapp.models import Category, Blog

# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = {
            
#         }
class BlogFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = {
            'category__name': ['exact'],
            'author__name': ['exact'],
            'created_at': ['lt', 'gt', 'exact'],
            'updated_at': ['lt', 'gt', 'exact'],
        }
