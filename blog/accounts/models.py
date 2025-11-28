from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default/default.png')

    def __str__(self):
        return self.username