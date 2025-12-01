from rest_framework import serializers
from django.core.validators import RegexValidator
from accounts.models import User
from baseapp.models import Category, Blog

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        validators=[RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-])[A-Za-z\d!@#$%^&*-]{8,32}$',
                message='The password must be 8-32 characters, include at least one lowercase, one uppercase, one digit, and one special character. (Allowed special characters: !@#$%%^&*-).'
        )]
    )
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'avatar', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug']

class BlogSerailizer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'description', 'image', 'author', 'category', 'created_at', 'updated_at']
        