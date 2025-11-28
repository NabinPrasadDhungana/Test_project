from django.db import models
from django.conf import settings 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=150, null=True)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title